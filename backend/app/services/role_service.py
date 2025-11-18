import httpx
import google.generativeai as genai
import json
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.core.config import settings
from app.db.models import TargetRoleProfile
from app.schemas.role import GeminiRoleProfileSchema

# Configure the Gemini client
genai.configure(api_key=settings.GOOGLE_API_KEY)

# Constants
CACHE_DURATION_DAYS = 7
ARBEITNOW_API_URL = "https://www.arbeitnow.com/api/job-board-api"
JOB_FETCH_LIMIT = 10 # Number of job descriptions to fetch

# --- 1. External API: Fetch Job Descriptions (with filtering) ---

async def get_job_descriptions(role_name: str) -> List[str]:
    """
    Fetches live job descriptions from the Arbeitnow API and
    filters them for relevance.
    """
    # Create normalized keywords from the role name
    # e.g., "React Developer" -> ["react", "developer"]
    keywords = role_name.strip().lower().split()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                ARBEITNOW_API_URL,
                params={"query": role_name, "page": 1}
            )
            response.raise_for_status() 
            data = response.json()
            
            filtered_jobs = []
            
            for job in data.get("data", []):
                job_title_lower = job.get("title", "").lower()
                job_description = job.get("description", "")

                # THE FIX: Check if all keywords are in the job title
                if job_description and all(keyword in job_title_lower for keyword in keywords):
                    filtered_jobs.append(job_description)

            if not filtered_jobs:
                # Fallback if our strict filter got 0 results
                descriptions = [
                    job.get("description", "") 
                    for job in data.get("data", []) 
                    if job.get("description")
                ]
                return [desc for desc in descriptions if desc][:JOB_FETCH_LIMIT]

            # Return a cleaned, limited list of *filtered* jobs
            return [desc for desc in filtered_jobs if desc][:JOB_FETCH_LIMIT]
            
        except httpx.HTTPStatusError as e:
            print(f"HTTP error fetching jobs: {e}")
            return []
        except Exception as e:
            print(f"Error fetching jobs: {e}")
            return []

# --- 2. AI Call: Synthesize Profile ---

async def get_ideal_profile_from_gemini(
    role_name: str, 
    job_descriptions: List[str]
) -> GeminiRoleProfileSchema | None:
    """
    Uses Gemini to synthesize an ideal profile from a list of job descriptions.
    """
    if not job_descriptions:
        return None

    # Combine descriptions into one large text block
    combined_descriptions = "\n\n---JOB SEPARATOR---\n\n".join(job_descriptions)

    # Set up the model for JSON output
    model = genai.GenerativeModel(
        'gemini-2.5-flash',
        generation_config={"response_mime_type": "application/json"}
    )
    
    prompt = f"""
    Analyze the following {len(job_descriptions)} job descriptions for a '{role_name}' position. 
    Based *only* on the text provided, synthesize an 'Ideal Candidate Profile'.
    
    Your response MUST be a JSON object matching this schema:
    {GeminiRoleProfileSchema.model_json_schema()}

    Job Descriptions:
    {combined_descriptions}
    """
    
    try:
        response = await model.generate_content_async(prompt)
        response_text = response.text
        
        # Parse and validate the JSON response using our Pydantic schema
        profile_data = GeminiRoleProfileSchema.model_validate_json(response_text)
        return profile_data
        
    except Exception as e:
        print(f"Error calling Gemini or validating JSON: {e}")
        print(f"Raw response was: {response_text if 'response_text' in locals() else 'N/A'}")
        return None

# --- 3. Main Service: Caching & Orchestration (with UPDATE logic) ---

async def get_or_create_role_profile(
    db: AsyncSession, 
    role_name: str
) -> TargetRoleProfile:
    """
    Main logic: Check cache, or fetch, generate, and save a new profile.
    If profile is stale, it will be updated.
    """
    # Sanitize role name
    normalized_role = role_name.strip().lower()

    # 1. Check for ANY existing profile, regardless of time
    result = await db.execute(
        select(TargetRoleProfile)
        .filter(TargetRoleProfile.role_name == normalized_role)
    )
    existing_profile = result.scalars().first()

    # 2. Check if it's fresh enough
    cache_cutoff = datetime.now(timezone.utc) - timedelta(days=CACHE_DURATION_DAYS)

    if existing_profile and existing_profile.created_at >= cache_cutoff:
        # It exists and is fresh, return it immediately.
        return existing_profile

    # 3. If it's stale (or doesn't exist), we must generate new data.
    job_descriptions = await get_job_descriptions(role_name)
    if not job_descriptions:
        raise Exception("Could not fetch job descriptions for this role.")

    gemini_profile = await get_ideal_profile_from_gemini(role_name, job_descriptions)
    if not gemini_profile:
        raise Exception("Failed to generate AI profile. Please try again.")

    # Prepare data
    all_skills = {
        "technical": gemini_profile.top_technical_skills,
        "soft": gemini_profile.top_soft_skills
    }
    source_info = {"source": "arbeitnow.com", "jobs_analyzed": len(job_descriptions)}

    # 4. THE KEY FIX: Update if it exists, Insert if it's new
    if existing_profile:
        # It's an UPDATE
        existing_profile.ideal_profile_text = gemini_profile.ideal_profile_summary
        existing_profile.top_skills_json = json.dumps(all_skills)
        existing_profile.source_job_examples = json.dumps(source_info)
        existing_profile.created_at = datetime.now(timezone.utc) # Update timestamp

        await db.commit()
        await db.refresh(existing_profile)
        return existing_profile
    else:
        # It's an INSERT
        new_profile = TargetRoleProfile(
            role_name=normalized_role,
            ideal_profile_text=gemini_profile.ideal_profile_summary,
            top_skills_json=json.dumps(all_skills),
            source_job_examples=json.dumps(source_info)
        )

        db.add(new_profile)
        await db.commit()
        await db.refresh(new_profile)
        return new_profile