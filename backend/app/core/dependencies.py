from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from pydantic import ValidationError

from app.db.database import get_db
from app.core.config import settings
from app.schemas.token import TokenData
from app.services import user_service
from app.db.models import User

# This tells FastAPI where to look for the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Decodes the JWT token, validates it, and returns the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the JWT
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # The "sub" (subject) of our token is the user's email
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        # Validate the token data
        token_data = TokenData(email=email)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    # Fetch the user from the database
    user = await user_service.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    
    return user