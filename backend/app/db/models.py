from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    resumes = relationship("Resume", back_populates="owner")
    # analyses = relationship("AnalysisHistory", back_populates="user") # For Phase B

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String, nullable=False)
    extracted_text = Column(Text, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="resumes")

class TargetRoleProfile(Base):
    __tablename__ = "target_role_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True, nullable=False)
    ideal_profile_text = Column(Text, nullable=False)
    top_skills_json = Column(Text, nullable=False) # Storing as JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    source_job_examples = Column(Text) # Storing list of source URLs as JSON string

# Optional: Phase B/C model
# class AnalysisHistory(Base):
#     __tablename__ = "analysis_history"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     resume_id = Column(Integer, ForeignKey("resumes.id"))
#     role_profile_id = Column(Integer, ForeignKey("target_role_profiles.id"))
#     result_json = Column(Text, nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
    
#     user = relationship("User", back_populates="analyses")