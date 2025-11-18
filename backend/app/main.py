from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth
from app.api import resume
from app.api import role
from app.api import skill_gap

app = FastAPI(
    title="SkillSync AI API",
    description="Analyzes resumes against job roles and builds learning roadmaps.",
    version="0.1.0"
)

# Configure CORS
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://skillsync-frontend-1078370935935.us-central1.run.app",
        
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the SkillSync AI API!"}

# We will add our API routers here in the next step
# from app.api.v1.endpoints import auth
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

# Include the auth router
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

app.include_router(resume.router, prefix="/resume", tags=["Resumes"])

app.include_router(role.router, prefix="/role", tags=["Role Analysis"])

app.include_router(skill_gap.router, prefix="/skill-gap", tags=["Skill Gap"])