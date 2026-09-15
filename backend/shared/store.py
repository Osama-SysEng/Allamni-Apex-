from dataclasses import dataclass, field
from uuid import uuid4
from shared.models import LearningProfile, Resource
from shared.memory import LearningMemory

@dataclass
class MemoryStore:
    # Phase 1 Collections
    users: dict = field(default_factory=dict)
    users_by_email: dict = field(default_factory=dict)
    profiles: dict = field(default_factory=dict)
    events: list = field(default_factory=list)
    resources: list = field(default_factory=list)
    outbox: list = field(default_factory=list)
    sessions: dict = field(default_factory=dict)
    consents: dict = field(default_factory=dict)
    assessment_attempts: dict = field(default_factory=dict)
    audit: list = field(default_factory=list)
    memory: LearningMemory = field(default_factory=LearningMemory)
    
    # Phase 1 New Collections
    institutions: dict = field(default_factory=dict)
    subscriptions: dict = field(default_factory=dict)
    student_codes: dict = field(default_factory=dict)
    teacher_codes: dict = field(default_factory=dict)
    institution_settings: dict = field(default_factory=dict)
    parent_student_relationships: dict = field(default_factory=dict)
    
    # Phase 2 New Collections
    invoices: dict = field(default_factory=dict)
    payments: dict = field(default_factory=dict)
    odoo_sync_events: dict = field(default_factory=dict)
    
    # Phase 3 New Collections
    learning_signals: dict = field(default_factory=dict)
    learning_patterns: dict = field(default_factory=dict)
    model_updates: dict = field(default_factory=dict)
    learning_metrics: dict = field(default_factory=dict)
    voice_interactions: dict = field(default_factory=dict)
    voice_sessions: dict = field(default_factory=dict)
    image_analyses: dict = field(default_factory=dict)
    
    # Phase 5 Enhanced Security Collections
    auth_sessions: dict = field(default_factory=dict)
    two_factor_auths: dict = field(default_factory=dict)
    biometric_auths: dict = field(default_factory=dict)
    security_events: dict = field(default_factory=dict)
    failed_login_attempts: dict = field(default_factory=dict)
    account_lockouts: dict = field(default_factory=dict)
    rate_limits: dict = field(default_factory=dict)
    security_incidents: dict = field(default_factory=dict)
    encrypted_data: dict = field(default_factory=dict)
    security_metrics: dict = field(default_factory=dict)
    
    # Phase 5 AI Chatbot Collections
    conversation_threads: dict = field(default_factory=dict)
    conversation_memories: dict = field(default_factory=dict)
    ai_knowledge_base: dict = field(default_factory=dict)
    conversation_analytics: dict = field(default_factory=dict)
    
    # Service references
    billing_service: object = None
    self_learning_pipeline: object = None
    voice_manager: object = None
    enhanced_auth_service: object = None
    advanced_security_service: object = None
    powerful_ai_chatbot: object = None

    def reset(self):
        """Reset all collections to initial state"""
        # Phase 1 collections
        self.users.clear()
        self.users_by_email.clear()
        self.profiles.clear()
        self.events.clear()
        self.resources.clear()
        self.outbox.clear()
        self.sessions.clear()
        self.consents.clear()
        self.assessment_attempts.clear()
        self.audit.clear()
        
        # Phase 1 new collections
        self.institutions.clear()
        self.subscriptions.clear()
        self.student_codes.clear()
        self.teacher_codes.clear()
        self.institution_settings.clear()
        self.parent_student_relationships.clear()
        
        # Phase 2 new collections
        self.invoices.clear()
        self.payments.clear()
        self.odoo_sync_events.clear()
        
        # Phase 3 new collections
        self.learning_signals.clear()
        self.learning_patterns.clear()
        self.model_updates.clear()
        self.learning_metrics.clear()
        self.voice_interactions.clear()
        self.voice_sessions.clear()
        self.image_analyses.clear()
        
        # Phase 5 enhanced security collections
        self.auth_sessions.clear()
        self.two_factor_auths.clear()
        self.biometric_auths.clear()
        self.security_events.clear()
        self.failed_login_attempts.clear()
        self.account_lockouts.clear()
        self.rate_limits.clear()
        self.security_incidents.clear()
        self.encrypted_data.clear()
        self.security_metrics.clear()
        
        # Phase 5 AI chatbot collections
        self.conversation_threads.clear()
        self.conversation_memories.clear()
        self.ai_knowledge_base.clear()
        self.conversation_analytics.clear()
        
        # Re-seed initial data
        self.seed()

    def seed(self):
        """Seed initial data for development"""
        self.resources.extend([
            Resource(id="res_1", title="Python Basics", platform="Khan Academy",
                     url="https://www.khanacademy.org/computing/computer-programming",
                     skills=["python_basics"], attributes=["video","interactive"],
                     duration_minutes=120, quality_score=.90),
            Resource(id="res_2", title="Object Oriented Programming", platform="Coursera",
                     url="https://www.coursera.org/", skills=["oop"],
                     attributes=["video","reading"], duration_minutes=180, quality_score=.88),
            Resource(id="res_3", title="Interactive OOP", platform="Codecademy",
                     url="https://www.codecademy.com/", skills=["oop"],
                     attributes=["interactive"], duration_minutes=90, quality_score=.91),
            Resource(id="res_4", title="Problem Solving", platform="freeCodeCamp",
                     url="https://www.freecodecamp.org/learn", skills=["problem_solving"],
                     attributes=["interactive","project"], duration_minutes=120, quality_score=.86),
            Resource(id="res_5", title="Data Structures", platform="edX",
                     url="https://www.edx.org/", skills=["data_structures"],
                     attributes=["video","reading"], duration_minutes=240, quality_score=.84),
        ])

# Global store instance
store = MemoryStore()
store.reset()