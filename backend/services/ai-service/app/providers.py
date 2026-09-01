from abc import ABC, abstractmethod
import os
from typing import Any

class LLMProvider(ABC):
    @abstractmethod
    def analyze(self, profile:dict)->dict: ...
    @abstractmethod
    def generate(self, prompt:str, context:dict)->dict: ...

class DeterministicProvider(LLMProvider):
    def analyze(self, profile):
        gaps=[s["code"] for s in profile.get("skills",[]) if s.get("target",0)>s.get("level",0)]
        return {"summary":"Deterministic adaptive analysis","gaps":gaps}
    def generate(self,prompt,context):
        return {"text":"Generated content requires configured LLM provider.","provider":"deterministic","prompt_hash":hash(prompt),"context_keys":list(context)}

def get_provider(name=None):
    # No fake claim of remote AI. Real providers can be added behind this contract.
    return DeterministicProvider()
