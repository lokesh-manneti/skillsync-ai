from pydantic import BaseModel, Field
from typing import List, Literal

# --- For the API Request ---

class SkillGapRequest(BaseModel):
    resume_id: int
    role_name: str
    learning_preference: Literal["Coding Projects", "Video Courses", "Reading / Docs"] = "Coding Projects"

# --- For the Gemini JSON Response ---
# We define the structure we want the AI to return.

class LearningStep(BaseModel):
    step_title: str = Field(description="A short, actionable title for this learning step.")
    estimated_hours: float = Field(description="Estimated hours to complete this single step.")
    details: str = Field(description="A 2-3 sentence explanation of what to do in this step.")

class SkillGapItem(BaseModel):
    skill_name: str = Field(description="The specific skill being analyzed (e.g., 'React', 'SQL', 'Teamwork').")
    match_status: Literal["Matched", "Missing", "Partial"] = Field(
        description="Whether the skill is matched, partially matched, or missing from the resume."
    )
    justification: str = Field(
        description="A 1-2 sentence justification for the match_status, referencing the resume or lack thereof."
    )
    learning_plan: List[LearningStep] | None = Field(
        description="A list of learning steps. This should be null if match_status is 'Matched', otherwise it must contain steps."
    )

class GeminiSkillGapSchema(BaseModel):
    """
    The root JSON schema for the skill gap analysis response from Gemini.
    """
    skill_match_score: float = Field(
        description="A score from 0.0 to 100.0 representing the resume's match to the ideal profile.",
        ge=0.0,
        le=100.0
    )
    analysis_summary: str = Field(
        description="A motivational 3-5 sentence summary of the user's strengths and key areas for improvement."
    )
    skill_comparison: List[SkillGapItem] = Field(
        description="A detailed list comparing the resume against the target skills."
    )

# --- For the API Response ---
# Our API will return the exact structure it gets from Gemini.
# So, we can just reuse the GeminiSkillGapSchema as our response_model.