"""
AI Provider Interface and Implementations for Allamni v4.0
Supports multiple AI providers with Gemini as primary
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel
import httpx
import json
import os

class AIProviderType(str, Enum):
    MOCK = "mock"
    GEMINI = "gemini"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class AIMessage(BaseModel):
    role: MessageRole
    content: str
    metadata: Dict[str, Any] = {}

class AIResponse(BaseModel):
    content: str
    model_used: str
    tokens_used: Optional[int] = None
    cost: Optional[float] = None
    latency_ms: Optional[int] = None
    metadata: Dict[str, Any] = {}

class BaseAIProvider(ABC):
    """Abstract base class for AI providers"""
    
    def __init__(self, api_key: str, model: str = None):
        self.api_key = api_key
        self.model = model
        self.client = httpx.AsyncClient(timeout=120.0)
    
    @abstractmethod
    async def generate(self, prompt: str, context: Dict[str, Any] = None) -> AIResponse:
        """Generate a response from the AI"""
        pass
    
    @abstractmethod
    async def chat(self, messages: List[AIMessage], context: Dict[str, Any] = None) -> AIResponse:
        """Chat with the AI using conversation history"""
        pass
    
    @abstractmethod
    async def analyze(self, data: Dict[str, Any]) -> AIResponse:
        """Analyze data and provide insights"""
        pass
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

class MockAIProvider(BaseAIProvider):
    """Mock provider for development and testing"""
    
    def __init__(self):
        super().__init__(api_key="mock", model="mock-model")
    
    async def generate(self, prompt: str, context: Dict[str, Any] = None) -> AIResponse:
        """Generate a mock response"""
        responses = [
            "هذا محتوى تعليمي تجريبي تم إنشاؤه بواسطة نظام المحاكاة.",
            "في التطبيق الحقيقي، سيتم استخدام Gemini API لإنشاء محتوى مخصص.",
            "هذا النظام يدعم اللغة العربية بشكل كامل مع لهجات مختلفة.",
        ]
        import random
        return AIResponse(
            content=random.choice(responses),
            model_used="mock-model",
            metadata={"provider": "mock", "context": context}
        )
    
    async def chat(self, messages: List[AIMessage], context: Dict[str, Any] = None) -> AIResponse:
        """Mock chat response"""
        last_message = messages[-1].content if messages else ""
        
        if "مرحبا" in last_message or "hello" in last_message.lower():
            response = "مرحباً بك! كيف يمكنني مساعدتك في رحلتك التعليمية اليوم؟"
        elif "ساعد" in last_message or "help" in last_message.lower():
            response = "بالتأكيد! أنا هنا لمساعدتك. ما الذي تحتاج إلى توضيح حوله؟"
        else:
            response = "شكراً لسؤالك. سأقوم بتقديم إجابة مفصلة وشاملة لك."
        
        return AIResponse(
            content=response,
            model_used="mock-model",
            metadata={"provider": "mock", "message_count": len(messages)}
        )
    
    async def analyze(self, data: Dict[str, Any]) -> AIResponse:
        """Mock analysis response"""
        return AIResponse(
            content="تحليل تجريبي: البيانات تبدو طبيعية ومتوافقة مع معايير النظام.",
            model_used="mock-model",
            metadata={"provider": "mock", "data_keys": list(data.keys())}
        )

class GeminiAIProvider(BaseAIProvider):
    """Google Gemini API provider for production"""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        super().__init__(api_key=api_key, model=model)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
    
    async def generate(self, prompt: str, context: Dict[str, Any] = None) -> AIResponse:
        """Generate content using Gemini API"""
        import time
        start_time = time.time()
        
        context = context or {}
        system_instruction = context.get('system_instruction', 
            "أنت معلم ذكي متخصص في التعليم للطلاب العرب. تتحدث العربية بطلاقة وتشرح المفاهيم بشكل واضح ومبسط.")
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048,
            }
        }
        
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }
        
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        
        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            content = data["candidates"][0]["content"]["parts"][0]["text"]
            tokens_used = data.get("usageMetadata", {}).get("totalTokenCount")
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            return AIResponse(
                content=content,
                model_used=self.model,
                tokens_used=tokens_used,
                latency_ms=latency_ms,
                metadata={"provider": "gemini", "raw_response": data}
            )
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    async def chat(self, messages: List[AIMessage], context: Dict[str, Any] = None) -> AIResponse:
        """Chat with Gemini using conversation history"""
        import time
        start_time = time.time()
        
        context = context or {}
        system_instruction = context.get('system_instruction',
            "أنت رفيق تعليمي ذكي للطلاب العرب. تتحدث العربية بطلاقة بلهجات مختلفة (مصرية، خليجية، شامية).")
        
        # Convert messages to Gemini format
        contents = []
        for msg in messages:
            role = "user" if msg.role == MessageRole.USER else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg.content}]
            })
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.8,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 4096,
            }
        }
        
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }
        
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        
        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            content = data["candidates"][0]["content"]["parts"][0]["text"]
            tokens_used = data.get("usageMetadata", {}).get("totalTokenCount")
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            return AIResponse(
                content=content,
                model_used=self.model,
                tokens_used=tokens_used,
                latency_ms=latency_ms,
                metadata={"provider": "gemini", "message_count": len(messages)}
            )
        except Exception as e:
            raise Exception(f"Gemini chat error: {str(e)}")
    
    async def analyze(self, data: Dict[str, Any]) -> AIResponse:
        """Analyze data using Gemini"""
        prompt = f"""
        قم بتحليل البيانات التعليمية التالية وقدم تقييماً شاملاً:
        
        البيانات: {json.dumps(data, ensure_ascii=False, indent=2)}
        
        قم بتقديم:
        1. ملخص للحالة الحالية
        2. نقاط القوة
        3. نقاط الضعف
        4. توصيات للتحسين
        """
        
        return await self.generate(prompt, {
            "system_instruction": "أنت محلل تعليمي خبير. تحلل البيانات وتقدم توصيات عملية باللغة العربية."
        })

def get_ai_provider(provider_type: AIProviderType = AIProviderType.MOCK, **kwargs) -> BaseAIProvider:
    """Factory function to get AI provider instance"""
    
    if provider_type == AIProviderType.MOCK:
        return MockAIProvider()
    
    elif provider_type == AIProviderType.GEMINI:
        api_key = kwargs.get('api_key') or os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required for Gemini provider")
        model = kwargs.get('model', 'gemini-1.5-pro')
        return GeminiAIProvider(api_key=api_key, model=model)
    
    elif provider_type == AIProviderType.OPENAI:
        # TODO: Implement OpenAI provider
        raise NotImplementedError("OpenAI provider not yet implemented")
    
    elif provider_type == AIProviderType.ANTHROPIC:
        # TODO: Implement Anthropic provider
        raise NotImplementedError("Anthropic provider not yet implemented")
    
    else:
        raise ValueError(f"Unknown provider type: {provider_type}")