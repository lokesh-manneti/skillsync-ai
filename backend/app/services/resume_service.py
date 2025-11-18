import io
import google.generativeai as genai
from app.core.config import settings
from PyPDF2 import PdfReader
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.models import Resume, User, TargetRoleProfile
from app.schemas.resume import ResumeCreate
from sqlalchemy.future import select

def extract_text_from_pdf(pdf_file: io.BytesIO) -> str:
    """
    Extracts text content from a PDF file.
    """
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        if not text:
            # Fallback for scanned/image-based PDFs
            return "Error: Could not extract text. The PDF might be image-based."
            
        return text
    except Exception as e:
        # Handle potential PyPDF2 errors
        return f"Error: Failed to process PDF file. {str(e)}"

async def create_resume(
    db: AsyncSession, 
    resume_data: ResumeCreate, 
    user: User
) -> Resume:
    """
    Saves a new resume record to the database.
    """
    db_resume = Resume(
        original_filename=resume_data.original_filename,
        extracted_text=resume_data.extracted_text,
        user_id=user.id  # Link to the current user
    )
    db.add(db_resume)
    await db.commit()
    await db.refresh(db_resume)
    return db_resume


async def generate_optimized_resume(
    resume_text: str,
    role_profile: TargetRoleProfile
) -> str:
    """
    Calls Gemini to rewrite a resume to be ATS-friendly and matched
    to the ideal profile.
    """
    model = genai.GenerativeModel('gemini-2.5-flash') # No JSON mode needed

    prompt = f"""
    You are an expert resume writer. Your task is to rewrite the provided resume
    to be ATS-friendly and highly aligned with the "Ideal Candidate Profile".

    **RULES:**
    - The output MUST be plain text only.
    - Do NOT use Markdown, HTML, or any formatting.
    - Rewrite the resume's "Summary" and "Experience" sections to use keywords
      and phrases from the "Ideal Candidate Profile".
    - Quantify achievements where possible.
    - Ensure the skills section includes skills from the "Ideal Profile".
    - The tone should be professional and confident.

    **IDEAL CANDIDATE PROFILE for {role_profile.role_name}:**
    ---
    {role_profile.ideal_profile_text}
    ---

    **USER'S CURRENT RESUME:**
    ---
    {resume_text}
    ---

    **ATS-OPTIMIZED RESUME (PLAIN TEXT):**
    """

    try:
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini for resume optimization: {e}")
        return "Error: Could not generate optimized resume."

async def get_resumes_by_user(db: AsyncSession, user: User) -> List[Resume]:
    """
    Fetches all resumes uploaded by a specific user.
    """
    result = await db.execute(
        select(Resume)
        .filter(Resume.user_id == user.id)
        .order_by(Resume.uploaded_at.desc())
    )
    return result.scalars().all()