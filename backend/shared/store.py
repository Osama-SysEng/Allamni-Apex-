from dataclasses import dataclass, field
from uuid import uuid4
from shared.models import LearningProfile, Resource
from shared.memory import LearningMemory

@dataclass
class MemoryStore:
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

    def reset(self):
        self.users.clear(); self.users_by_email.clear(); self.profiles.clear()
        self.events.clear(); self.resources.clear(); self.outbox.clear(); self.sessions.clear(); self.consents.clear(); self.assessment_attempts.clear(); self.audit.clear()
        self.seed()

    def seed(self):
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

store = MemoryStore()
store.reset()
