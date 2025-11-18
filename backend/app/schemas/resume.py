from pydantic import BaseModel
from datetime import datetime

class ResumeBase(BaseModel):
    original_filename: str
    
class ResumeCreate(ResumeBase):
    extracted_text: str

class Resume(ResumeBase):
    id: int
    user_id: int
    uploaded_at: datetime
    extracted_text_preview: str # We'll send a preview, not the whole text

    class Config:
        from_attributes = True

class ResumeUploadResponse(BaseModel):
    resume_id: int
    original_filename: str
    extracted_text_preview: str

class ResumeOptimizeRequest(BaseModel):
    resume_id: int
    role_name: str

class ResumeOptimizeResponse(BaseModel):
    optimized_resume_text: str

class ResumeInfo(BaseModel):
    """
    Schema for displaying a list of resumes.
    """
    id: int
    original_filename: str
    uploaded_at: datetime

    class Config:
        from_attributes = True