import io
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import User
from app.core.dependencies import get_current_user
from app.schemas.resume import ResumeCreate, ResumeUploadResponse
from app.services import resume_service

from app.schemas.resume import ResumeOptimizeRequest, ResumeOptimizeResponse
from app.services import role_service, skill_gap_service

from typing import List
# Add your new schema
from app.schemas.resume import ResumeInfo

router = APIRouter()


@router.get(
    "/history", 
    response_model=List[ResumeInfo],
    tags=["Resumes"]
)
async def get_resume_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves a list of all resumes uploaded by the current user.
    """
    resumes = await resume_service.get_resumes_by_user(db, user=current_user)
    return resumes


@router.post("/upload", response_model=ResumeUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a resume PDF, extract its text, and save it for the user.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF files are accepted."
        )

    try:
        # Read file content into memory
        file_content = await file.read()
        file_stream = io.BytesIO(file_content)

        # Extract text
        extracted_text = resume_service.extract_text_from_pdf(file_stream)
        
        if extracted_text.startswith("Error:"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=extracted_text
            )

        # Create the resume schema
        resume_data = ResumeCreate(
            original_filename=file.filename,
            extracted_text=extracted_text
        )

        # Save to database
        new_resume = await resume_service.create_resume(
            db=db, resume_data=resume_data, user=current_user
        )

        # Return a preview of the text (e.g., first 500 chars)
        preview = (extracted_text[:500] + '...') if len(extracted_text) > 500 else extracted_text
        
        return ResumeUploadResponse(
            resume_id=new_resume.id,
            original_filename=new_resume.original_filename,
            extracted_text_preview=preview
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    finally:
        await file.close()

@router.post("/optimize", response_model=ResumeOptimizeResponse)
async def optimize_resume(
    request: ResumeOptimizeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generates an ATS-optimized version of a user's resume
    based on a target role.
    """
    # 1. Get the user's resume
    resume = await skill_gap_service.get_resume_by_id(
        db, resume_id=request.resume_id, user=current_user
    )
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found."
        )

    # 2. Get the target role profile
    try:
        role_profile = await role_service.get_or_create_role_profile(
            db, role_name=request.role_name
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to analyze role: {str(e)}"
        )

    # 3. Call AI to generate the optimized text
    optimized_text = await resume_service.generate_optimized_resume(
        resume_text=resume.extracted_text,
        role_profile=role_profile
    )

    return ResumeOptimizeResponse(optimized_resume_text=optimized_text)