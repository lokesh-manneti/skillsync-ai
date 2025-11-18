from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import User
from app.core.dependencies import get_current_user
from app.schemas.skill_gap import SkillGapRequest, GeminiSkillGapSchema
from app.services import skill_gap_service, role_service

router = APIRouter()

@router.post(
    "/analyze", 
    response_model=GeminiSkillGapSchema,
    tags=["Skill Gap"]
)
async def analyze_skill_gap(
    request: SkillGapRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Performs a full skill-gap analysis by comparing a user's resume
    against an ideal role profile and generates a learning plan.
    """
    
    # 1. Get the user's resume
    resume = await skill_gap_service.get_resume_by_id(
        db, resume_id=request.resume_id, user=current_user
    )
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found or does not belong to user."
        )
    
    # 2. Get the target role profile (from cache or new)
    try:
        role_profile = await role_service.get_or_create_role_profile(
            db, role_name=request.role_name
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to analyze role: {str(e)}"
        )

    # 3. Call the AI service to generate the analysis
    try:
        analysis_result = await skill_gap_service.generate_skill_gap_analysis(
            resume_text=resume.extracted_text,
            role_profile=role_profile,
            learning_preference=request.learning_preference
        )
        return analysis_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate skill gap analysis: {str(e)}"
        )

# ---
# Note: In our original plan, we had /resume/skill-gap
# I'm creating a new file /api/skill_gap.py with a route /analyze
# We can mount this as /skill-gap/analyze in main.py
# ---