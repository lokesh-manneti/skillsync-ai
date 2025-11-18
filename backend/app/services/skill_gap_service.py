import json
import google.generativeai as genai
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.db.models import Resume, TargetRoleProfile, User
from app.schemas.skill_gap import GeminiSkillGapSchema, SkillGapRequest

# Configure the Gemini client
genai.configure(api_key=settings.GOOGLE_API_KEY)

async def get_resume_by_id(db: AsyncSession, resume_id: int, user: User) -> Resume:
    """
    Fetches a specific resume by its ID, ensuring it belongs to the current user.
    """
    result = await db.execute(
        select(Resume).filter(Resume.id == resume_id, Resume.user_id == user.id)
    )
    resume = result.scalars().first()
    return resume

async def generate_skill_gap_analysis(
    resume_text: str,
    role_profile: TargetRoleProfile,
    learning_preference: str
) -> GeminiSkillGapSchema:
    """
    Calls Gemini to perform the skill gap analysis.
    """
    
    # Set up the model for JSON output
    model = genai.GenerativeModel(
        'gemini-2.5-flash',
        generation_config={"response_mime_type": "application/json"}
    )
    
    # Get the target skills from the role profile
    # The 'top_skills_json' is a string, so we parse it
    target_skills_data = json.loads(role_profile.top_skills_json)
    target_skills_list = target_skills_data.get("technical", []) + target_skills_data.get("soft", [])
    
    prompt = f"""
    You are "SkillSync AI," an expert career mentor. Your job is to perform a detailed skill-gap analysis.

    **USER'S RESUME:**
    ---
    {resume_text}
    ---

    **IDEAL CANDIDATE PROFILE for {role_profile.role_name}:**
    ---
    {role_profile.ideal_profile_text}
    ---

    **KEY TARGET SKILLS for {role_profile.role_name}:**
    {', '.join(target_skills_list)}

    **USER'S LEARNING PREFERENCE:**
    {learning_preference}

    **YOUR TASK:**
    Analyze the resume against the ideal profile and key skills. Return a JSON object matching this *exact* schema.

    **JSON SCHEMA:**
    {GeminiSkillGapSchema.model_json_schema()}

    **INSTRUCTIONS:**
    1.  **skill_match_score**: Calculate a score (0.0-100.0) based on how well the resume matches the *ideal profile* and *key skills*.
    2.  **analysis_summary**: Write a motivational summary. Highlight strengths and the top 2-3 skills to learn.
    3.  **skill_comparison**:
        * Iterate through *all* skills in the "KEY TARGET SKILLS" list.
        * For each skill, set `match_status` ('Matched', 'Partial', 'Missing').
        * Write a `justification` explaining *why* (e.g., "Matched: 'React' is listed under Projects section.").
        * If `match_status` is 'Missing' or 'Partial', provide a `learning_plan` with 3-5 steps.
        * **Crucially**: The `learning_plan` steps must align with the user's `learning_preference` ('{learning_preference}').
            * If 'Coding Projects', steps should be: "1. Build a small to-do app...", "2. Add React Router...".
            * If 'Video Courses', steps should be: "1. Watch a 10-hour React course on...", "2. Complete the exercises...".
            * If 'Reading / Docs', steps should be: "1. Read the official React quick-start guide...", "2. Review API docs for Hooks...".
        * If `match_status` is 'Matched', `learning_plan` *must* be `null`.
    4.  Estimate `estimated_hours` for each learning step realistically.
    """
    
    try:
        response = await model.generate_content_async(prompt)
        response_text = response.text
        
        # --- THIS IS THE FIX ---
        # Clean the response: remove leading/trailing whitespace and
        # any "```json" or "```" markdown wrappers Gemini might add.
        sanitized_text = response_text.strip().strip("```json").strip("```").strip()
        # --- END FIX ---

        # Parse and validate the CLEANED response
        analysis_data = GeminiSkillGapSchema.model_validate_json(sanitized_text)
        return analysis_data
        
    except Exception as e:
        print(f"Error calling Gemini or validating skill-gap JSON: {e}")
        # In a real app, you might want to retry or handle this more gracefully
        # For debugging:
        print(f"Raw response from Gemini: {response_text if 'response_text' in locals() else 'N/A'}")
        raise Exception(f"Failed to get valid analysis from AI. {str(e)}")