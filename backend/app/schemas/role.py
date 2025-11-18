from pydantic import BaseModel, Field
from typing import List

# --- For Gemini's JSON Mode ---

class GeminiRoleProfileSchema(BaseModel):
    """
    The exact JSON schema we expect from Gemini.
    """
    ideal_profile_summary: str = Field(
        description="A 3-5 sentence summary of the ideal candidate, written as if for a job description."
    )
    top_technical_skills: List[str] = Field(
        description="A list of 5-10 specific technical skills (e.g., 'React', 'Node.js', 'SQL')."
    )
    top_soft_skills: List[str] = Field(
        description="A list of 3-5 key soft skills (e.g., 'Communication', 'Teamwork')."
    )

# --- For our API ---

class RoleAnalyzeRequest(BaseModel):
    role_name: str

class RoleAnalyzeResponse(BaseModel):
    id: int
    role_name: str
    ideal_profile_text: str
    top_skills_json: str # We'll return the JSON string of all skills

    class Config:
        from_attributes = True