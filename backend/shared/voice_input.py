"""
Voice Input Processing for Allamni v4.0
Handles speech-to-text and voice interaction features
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Optional, Any
from enum import Enum
import base64

class VoiceLanguage(str, Enum):
    """Supported languages for voice input"""
    ARABIC = "ar"
    ENGLISH = "en"
    FRENCH = "fr"
    GERMAN = "de"

class VoiceQuality(str, Enum):
    """Quality assessment of voice input"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    POOR = "poor"

@dataclass
class VoiceTranscription:
    """Result of voice transcription"""
    id: str
    user_id: str
    audio_data: str  # Base64 encoded audio
    transcribed_text: str
    language: VoiceLanguage
    confidence: float
    duration_seconds: float
    quality: VoiceQuality
    timestamp: datetime
    detected_dialect: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'transcribed_text': self.transcribed_text,
            'language': self.language.value,
            'confidence': self.confidence,
            'duration_seconds': self.duration_seconds,
            'quality': self.quality.value,
            'timestamp': self.timestamp.isoformat(),
            'detected_dialect': self.detected_dialect,
            'metadata': self.metadata
        }

class VoiceInputProcessor:
    """Voice input processing service"""
    
    def __init__(self):
        # Initialize voice processing resources
        self._init_speech_recognizer()

    def _init_speech_recognizer(self):
        """Initialize speech recognition engine"""
        # Rule-based stub: real STT (Google/Azure/Transcribe) needs credentials + user audio.
        self._recognizer_ready = True

    def transcribe_audio(self, audio_data: str, language: VoiceLanguage = VoiceLanguage.ARABIC,
                         user_id: str = None) -> VoiceTranscription:
        """Transcribe audio data to text"""
        if not audio_data or not isinstance(audio_data, str):
            raise ValueError("audio_data must be a non-empty base64 string")
        if not isinstance(language, VoiceLanguage):
            raise ValueError(f"language must be a VoiceLanguage (got {language!r})")
        
        transcription_id = str(uuid4())
        
        # Simulate transcription
        if language == VoiceLanguage.ARABIC:
            transcribed_text = "Sample Arabic transcription from speech to text"
            detected_dialect = "egyptian"
        else:
            transcribed_text = "This is a sample transcription from speech to text"
            detected_dialect = None
        
        # Simulate quality assessment
        confidence = 0.92
        quality = VoiceQuality.HIGH
        duration = 5.5  # Simulated duration
        
        transcription = VoiceTranscription(
            id=transcription_id,
            user_id=user_id or "unknown",
            audio_data=audio_data,
            transcribed_text=transcribed_text,
            language=language,
            confidence=confidence,
            duration_seconds=duration,
            quality=quality,
            timestamp=datetime.now(timezone.utc),
            detected_dialect=detected_dialect,
            metadata={
                'processing_time': 1.2,
                'model_used': 'rule_based_stt_stub_v1',
                'note': 'Deterministic stub: connect an STT service + user audio for production.'
            }
        )
        
        return transcription
    
    _LANGUAGE_ALIASES = {
        'ar': 'ar', 'arabic': 'ar', 'arab': 'ar', 'العربية': 'ar',
        'en': 'en', 'english': 'en', 'الإنجليزية': 'en',
        'fr': 'fr', 'french': 'fr', 'الفرنسية': 'fr',
        'de': 'de', 'german': 'de', 'الألمانية': 'de',
    }

    def process_voice_command(self, audio_data: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process voice command with context"""
        if not audio_data or not isinstance(audio_data, str):
            raise ValueError("audio_data must be a non-empty base64 string")
        if not isinstance(context, dict):
            raise ValueError("context must be a dict")
        # Transcribe audio (accept 'ar' or 'arabic' style language labels)
        raw_language = str(context.get('language', 'ar')).strip().lower()
        lang_code = self._LANGUAGE_ALIASES.get(raw_language, 'ar')
        try:
            language = VoiceLanguage(lang_code)
        except ValueError:
            raise ValueError(f"Unsupported language '{raw_language}'. Supported: ar, en, fr, de.")
        transcription = self.transcribe_audio(audio_data, language)
        
        # Analyze transcribed text for commands
        command = self._extract_command(transcription.transcribed_text, context)
        
        return {
            'transcription': transcription.to_dict(),
            'command': command,
            'success': command is not None
        }
    
    def _extract_command(self, text: str, context: Dict[str, Any]) -> Optional[str]:
        """Extract command from transcribed text"""
        # Simplified command extraction
        # In production, would use NLP for intent recognition
        
        command_keywords = {
            'explain': 'explain',
            'help': 'help',
            'quiz': 'quiz',
            'course': 'course',
            'progress': 'progress',
            'what': 'what'
        }
        
        text_lower = text.lower()
        for keyword, command in command_keywords.items():
            if keyword in text_lower:
                return command
        
        return None
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return [lang.value for lang in VoiceLanguage]
    
    def estimate_quality(self, audio_data: str) -> VoiceQuality:
        """Estimate audio quality from audio data"""
        # Placeholder implementation
        # In production, would analyze audio features like:
        # - Signal-to-noise ratio
        # - Background noise
        # - Clarity
        # - Volume levels
        
        return VoiceQuality.MEDIUM

class VoiceInteractionManager:
    """Manages voice interactions and context"""
    
    def __init__(self, store):
        self.store = store
        # Initialize voice collections if not exist
        if not hasattr(store, 'voice_interactions'):
            store.voice_interactions = {}
        if not hasattr(store, 'voice_sessions'):
            store.voice_sessions = {}
    
    def start_voice_session(self, user_id: str, context: Dict[str, Any] = None) -> str:
        """Start a new voice interaction session"""
        session_id = str(uuid4())
        
        session = {
            'id': session_id,
            'user_id': user_id,
            'context': context or {},
            'started_at': datetime.now(timezone.utc).isoformat(),
            'ended_at': None,
            'interactions': [],
            'total_duration': 0.0
        }
        
        self.store.voice_sessions[session_id] = session
        
        return session_id
    
    def add_interaction(self, session_id: str, transcription: VoiceTranscription) -> None:
        """Add a voice interaction to a session"""
        if session_id not in self.store.voice_sessions:
            return None
        
        session = self.store.voice_sessions[session_id]
        
        interaction = {
            'id': str(uuid4()),
            'transcription_id': transcription.id,
            'text': transcription.transcribed_text,
            'duration': transcription.duration_seconds,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        session['interactions'].append(interaction)
        session['total_duration'] += transcription.duration_seconds
        
        # Store interaction
        self.store.voice_interactions[interaction['id']] = interaction
    
    def end_voice_session(self, session_id: str) -> Dict[str, Any]:
        """End a voice session and return summary"""
        if session_id not in self.store.voice_sessions:
            return None
        
        session = self.store.voice_sessions[session_id]
        session['ended_at'] = datetime.now(timezone.utc).isoformat()
        
        return {
            'session_id': session_id,
            'user_id': session['user_id'],
            'duration': session['total_duration'],
            'interaction_count': len(session['interactions']),
            'started_at': session['started_at'],
            'ended_at': session['ended_at']
        }
    
    def get_user_voice_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get voice interaction history for a user"""
        if not user_id or not isinstance(user_id, str):
            raise ValueError("user_id must be a non-empty string")
        try:
            limit = int(limit)
        except (TypeError, ValueError):
            raise ValueError("limit must be an integer")
        limit = max(1, min(limit, 100))
        user_sessions = [
            session for session in self.store.voice_sessions.values()
            if session['user_id'] == user_id
        ]
        
        # Sort by start time descending
        user_sessions.sort(key=lambda x: x['started_at'], reverse=True)
        
        return user_sessions[:limit]

# Factory functions
def get_voice_processor() -> VoiceInputProcessor:
    """Get voice input processor instance"""
    return VoiceInputProcessor()

def get_voice_manager(store) -> VoiceInteractionManager:
    """Get voice interaction manager instance"""
    if not hasattr(store, 'voice_manager'):
        store.voice_manager = VoiceInteractionManager(store)
    return store.voice_manager