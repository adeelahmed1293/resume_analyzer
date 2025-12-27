# schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class CategoryScore(BaseModel):
    category: str = Field(description="Resume evaluation category name")
    score: int = Field(description="Score for this category", ge=0, le=100)

class ResumeAnalysis(BaseModel):
    overall_score: int = Field(description="Overall resume score (0–100)", ge=0, le=100)
    category_scores: List[CategoryScore] = Field(description="Category-wise resume scores")
    strengths: List[str] = Field(description="Key strengths of the resume as concise bullet points")
    improvements_needed: List[str] = Field(description="Areas where the resume needs improvement")
    actionable_suggestions: List[str] = Field(description="Clear and concise suggestions to improve the resume")





class User_data(BaseModel):
    email: EmailStr
    thread_ids: List[str] = []



class UserResponse(BaseModel):
    id: str
    email: EmailStr
    thread_ids: List[str] = []


# ---------------- Request Schemas ----------------
class ChatRequest(BaseModel):
    message: str
    email: EmailStr
    thread_id: Optional[str] = None  # Optional: if not provided, backend generates a new one

# ---------------- Response Schemas ----------------
class ChatResponse(BaseModel):
    thread_id: str
    response: str

class ChatHistoryResponse(BaseModel):
    thread_id: str
    messages: List  

class UserThreadsResponse(BaseModel):
    thread_ids: List


