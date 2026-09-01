from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class UserRole(str, Enum):
    STUDENT = "student"
    ADMIN = "admin"
    INSTITUTION_MANAGER = "institution_manager"

class Skill(BaseModel):
    code: str
    name: str
    level: float = Field(ge=0, le=1)
    target: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    importance: float = Field(default=1.0, ge=0)

class LearningPreferences(BaseModel):
    content_format: list[str] = Field(default_factory=list)
    pace: str = "self_paced"
    language: str = "ar"

class LearningProfile(BaseModel):
    student_id: str
    goal_domain: str
    learning_preferences: LearningPreferences = Field(default_factory=LearningPreferences)
    skills: list[Skill] = []

class Resource(BaseModel):
    id: str
    title: str
    platform: str
    url: str
    skills: list[str] = []
    attributes: list[str] = []
    duration_minutes: Optional[int] = None
    quality_score: float = Field(default=0.5, ge=0, le=1)

class RoadmapNode(BaseModel):
    id: str
    skill_code: str
    title: str
    sequence: int
    priority: float
    mastery_current: float
    mastery_target: float
    status: str = "pending"

class AssessmentQuestion(BaseModel):
    id: str
    skill_code: str
    question: str
    options: list[str]
    correct_index: int
    difficulty: float = 0.5

class AssessmentSubmission(BaseModel):
    question_id: str
    selected_index: int

class Recommendation(BaseModel):
    action_type: str
    message: str
    skill_code: Optional[str] = None
    resource: Optional[Resource] = None
    score: float = 0
    reasons: list[str] = []

class TeacherProfile(BaseModel):
    teacher_id: str
    subjects: list[str] = Field(default_factory=list)
    teaching_strengths: list[str] = Field(default_factory=list)
    teaching_preferences: list[str] = Field(default_factory=list)
    cognitive_signals: dict = {}

class ContentRequest(BaseModel):
    skill_code: str
    age_band: str = "all"
    language: str = "ar"
    formats: list[str] = ["mind_map", "interactive_game", "video", "image"]

class AdaptiveQuestion(BaseModel):
    id: str
    skill_code: str
    question: str
    options: list[str]
    correct_index: int
    difficulty: float = Field(ge=0.05, le=0.95)
    explanation: str = ""
    tags: list[str] = []
