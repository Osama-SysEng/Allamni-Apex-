from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID

class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"
    INSTITUTION_ADMIN = "institution_admin"
    SUPER_ADMIN = "super_admin"

class InstitutionType(str, Enum):
    SCHOOL = "school"
    UNIVERSITY = "university"
    TRAINING_CENTER = "training_center"

class SubscriptionPlan(str, Enum):
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"

class SubscriptionStatus(str, Enum):
    TRIAL = "trial"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"

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

# Institution Models
class Institution(BaseModel):
    id: UUID
    name_ar: str
    name_en: str
    type: InstitutionType
    sub_type: Optional[str] = None
    country: str
    city: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    admin_user_id: Optional[UUID] = None

class Subscription(BaseModel):
    id: UUID
    institution_id: UUID
    plan_type: SubscriptionPlan
    status: SubscriptionStatus
    start_date: date
    end_date: date
    max_students: Optional[int] = None
    max_teachers: Optional[int] = None
    max_admins: int = 1
    features: dict = {}
    billing_cycle: str = "monthly"
    auto_renew: bool = False
    created_at: datetime
    updated_at: datetime

class StudentCode(BaseModel):
    id: UUID
    institution_id: UUID
    code: str
    student_id: Optional[UUID] = None
    class_id: Optional[str] = None
    grade_level: Optional[str] = None
    academic_year: Optional[str] = None
    is_active: bool = True
    issued_by: Optional[UUID] = None
    issued_at: datetime
    used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    metadata: dict = {}

class TeacherCode(BaseModel):
    id: UUID
    institution_id: UUID
    code: str
    teacher_id: Optional[UUID] = None
    department: Optional[str] = None
    subjects: List[str] = []
    grade_levels: List[str] = []
    is_active: bool = True
    issued_by: Optional[UUID] = None
    issued_at: datetime
    used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    metadata: dict = {}

class InstitutionSettings(BaseModel):
    id: UUID
    institution_id: UUID
    branding: dict = {}
    content_policies: dict = {}
    language_preferences: str = "ar"
    timezone: str = "Africa/Cairo"
    academic_calendar: dict = {}
    notification_settings: dict = {}
    integration_settings: dict = {}
    created_at: datetime
    updated_at: datetime

class ParentStudentRelationship(BaseModel):
    id: UUID
    parent_id: UUID
    student_id: UUID
    relationship_type: str
    is_primary: bool = False
    can_view_progress: bool = True
    can_view_attendance: bool = True
    can_communicate: bool = True
    created_at: datetime
    updated_at: datetime

# Permission System
class Permission(BaseModel):
    resource: str
    action: str
    scope: str = "own"  # own, institution, all

class PermissionMatrix(BaseModel):
    role: UserRole
    permissions: List[Permission]

# Registration Models
class InstitutionRegistrationRequest(BaseModel):
    name_ar: str
    name_en: str
    type: InstitutionType
    sub_type: Optional[str] = None
    country: str
    city: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    admin_name: str
    admin_email: str
    admin_phone: str
    plan_type: SubscriptionPlan = SubscriptionPlan.BASIC

class StudentCodeRegistrationRequest(BaseModel):
    code: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    password: str = Field(min_length=8)
    date_of_birth: Optional[date] = None
    guardian_contact: Optional[str] = None

class TeacherCodeRegistrationRequest(BaseModel):
    code: str
    full_name: str
    email: str
    phone: str
    password: str = Field(min_length=8)
    specialization: Optional[str] = None
    qualifications: Optional[str] = None

class SelfRegistrationRequest(BaseModel):
    full_name: str
    email: str
    phone: str
    password: str = Field(min_length=8)
    role: UserRole = UserRole.STUDENT
    level: Optional[str] = None
    goals: List[str] = []
