from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import User
from app.core.dependencies import get_current_user
from app.schemas.role import RoleAnalyzeRequest, RoleAnalyzeResponse
from app.services import role_service

router = APIRouter()

@router.post("/analyze", response_model=RoleAnalyzeResponse)
async def analyze_role(
    request: RoleAnalyzeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user) # Secure this endpoint
):
    """
    Analyzes a job role by fetching live data, generating an AI profile,
    and caching the result.
    """
    try:
        profile = await role_service.get_or_create_role_profile(
            db=db, 
            role_name=request.role_name
        )
        
        return RoleAnalyzeResponse(
            id=profile.id,
            role_name=profile.role_name,
            ideal_profile_text=profile.ideal_profile_text,
            top_skills_json=profile.top_skills_json
        )
        
    except Exception as e:
        # Catch errors from the service (e.g., job fetching failed)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to analyze role: {str(e)}"
        )