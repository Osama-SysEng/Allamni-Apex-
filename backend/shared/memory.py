"""
Enhanced Learning Memory System for Allamni v4.0
Stores and retrieves learning interactions, preferences, and progress
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from typing import Dict, List, Optional, Any
from enum import Enum
import json

class MemoryType(str, Enum):
    """Types of memories stored"""
    CONVERSATION = "conversation"
    ASSESSMENT = "assessment"
    CONTENT_PLAN = "content_plan"
    MISTAKE = "mistake"
    PREFERENCE = "preference"
    ACHIEVEMENT = "achievement"
    QUESTION = "question"
    VOICE_INTERACTION = "voice_interaction"
    IMAGE_ANALYSIS = "image_analysis"

class MemoryImportance(str, Enum):
    """Importance levels for memory retention"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class MemoryItem:
    """A single memory item"""
    id: str
    user_id: str
    memory_type: MemoryType
    content: Dict[str, Any]
    importance: MemoryImportance
    timestamp: datetime
    expires_at: Optional[datetime] = None
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None  # For semantic search
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'memory_type': self.memory_type.value,
            'content': self.content,
            'importance': self.importance.value,
            'timestamp': self.timestamp.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'access_count': self.access_count,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'tags': self.tags,
            'metadata': self.metadata
        }

class LearningMemory:
    """Enhanced learning memory system"""
    
    def __init__(self):
        self.memories: Dict[str, MemoryItem] = {}
        self.user_indexes: Dict[str, List[str]] = {}  # user_id -> memory_ids
        self.type_indexes: Dict[str, List[str]] = {}  # memory_type -> memory_ids
        self.tag_indexes: Dict[str, List[str]] = {}  # tag -> memory_ids
        # Backward compatibility
        self._items: List[Dict] = []
    
    def remember(self, user_id: str, memory_type: str, content: Dict[str, Any], 
                 importance: str = "medium", tags: List[str] = None, 
                 expires_days: int = None, metadata: Dict[str, Any] = None) -> str:
        """Store a memory item"""
        if not user_id or not isinstance(user_id, str):
            raise ValueError("user_id must be a non-empty string")
        if not isinstance(content, dict) or not content:
            raise ValueError("content must be a non-empty dict")
        if expires_days is not None and expires_days <= 0:
            raise ValueError("expires_days must be a positive integer")
        memory_id = str(uuid4())
        
        # Convert string enums to enum objects
        try:
            mem_type = MemoryType(memory_type)
            imp_level = MemoryImportance(importance)
        except ValueError:
            mem_type = MemoryType.CONVERSATION
            imp_level = MemoryImportance.MEDIUM
        
        # Calculate expiration
        expires_at = None
        if expires_days:
            expires_at = datetime.now(timezone.utc) + timedelta(days=expires_days)
        
        # Create memory item
        memory = MemoryItem(
            id=memory_id,
            user_id=user_id,
            memory_type=mem_type,
            content=content,
            importance=imp_level,
            timestamp=datetime.now(timezone.utc),
            expires_at=expires_at,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        # Store memory
        self.memories[memory_id] = memory
        
        # Update indexes
        if user_id not in self.user_indexes:
            self.user_indexes[user_id] = []
        self.user_indexes[user_id].append(memory_id)
        
        if mem_type.value not in self.type_indexes:
            self.type_indexes[mem_type.value] = []
        self.type_indexes[mem_type.value].append(memory_id)
        
        for tag in memory.tags:
            if tag not in self.tag_indexes:
                self.tag_indexes[tag] = []
            self.tag_indexes[tag].append(memory_id)
        
        return memory_id
    
    def recall(self, user_id: str, memory_type: str = None, limit: int = 10, 
                tags: List[str] = None, importance: str = None) -> List[Dict]:
        """Recall memories for a user"""
        if not user_id or not isinstance(user_id, str):
            raise ValueError("user_id must be a non-empty string")
        # Clamp limit to a sane range (prevents unbounded reads)
        try:
            limit = int(limit)
        except (TypeError, ValueError):
            raise ValueError("limit must be an integer")
        limit = max(1, min(limit, 1000))
        # Normalize enum-or-string memory_type to its plain string value
        if memory_type is not None and isinstance(memory_type, Enum):
            memory_type = memory_type.value
        # Get user's memory IDs
        user_memory_ids = self.user_indexes.get(user_id, [])
        
        # Filter by type if specified
        if memory_type:
            type_ids = self.type_indexes.get(memory_type, [])
            user_memory_ids = [mid for mid in user_memory_ids if mid in type_ids]
        
        # Filter by tags if specified
        if tags:
            tag_ids = set()
            for tag in tags:
                tag_ids.update(self.tag_indexes.get(tag, []))
            user_memory_ids = [mid for mid in user_memory_ids if mid in tag_ids]
        
        # Filter by importance if specified
        if importance:
            try:
                importance_level = MemoryImportance(importance.value if isinstance(importance, Enum) else importance)
            except ValueError:
                valid = sorted(m.value for m in MemoryImportance)
                raise ValueError(f"Invalid importance '{importance}'. Valid values: {valid}")
            user_memory_ids = [
                mid for mid in user_memory_ids
                if self.memories[mid].importance == importance_level
            ]
        
        # Filter expired memories
        current_time = datetime.now(timezone.utc)
        user_memory_ids = [
            mid for mid in user_memory_ids
            if not self.memories[mid].expires_at or self.memories[mid].expires_at > current_time
        ]
        
        # Sort by importance and recency
        importance_order = {
            MemoryImportance.CRITICAL: 0,
            MemoryImportance.HIGH: 1,
            MemoryImportance.MEDIUM: 2,
            MemoryImportance.LOW: 3
        }
        
        user_memory_ids.sort(key=lambda mid: (
            importance_order.get(self.memories[mid].importance, 2),
            -self.memories[mid].timestamp.timestamp()
        ))
        
        # Update access count and last accessed
        for memory_id in user_memory_ids[:limit]:
            self.memories[memory_id].access_count += 1
            self.memories[memory_id].last_accessed = datetime.now(timezone.utc)
        
        # Return as dicts
        return [self.memories[mid].to_dict() for mid in user_memory_ids[:limit]]
    
    def forget(self, user_id: str, memory_id: str) -> bool:
        """Remove a specific memory"""
        if memory_id not in self.memories:
            return False
        
        memory = self.memories[memory_id]
        
        # Check ownership
        if memory.user_id != user_id:
            return False
        
        # Remove from indexes
        if user_id in self.user_indexes:
            self.user_indexes[user_id] = [mid for mid in self.user_indexes[user_id] if mid != memory_id]
        
        if memory.memory_type.value in self.type_indexes:
            self.type_indexes[memory.memory_type.value] = [
                mid for mid in self.type_indexes[memory.memory_type.value] if mid != memory_id
            ]
        
        for tag in memory.tags:
            if tag in self.tag_indexes:
                self.tag_indexes[tag] = [mid for mid in self.tag_indexes[tag] if mid != memory_id]
        
        # Remove memory
        del self.memories[memory_id]
        
        return True
    
    def search_semantic(self, user_id: str, query: str, limit: int = 5) -> List[Dict]:
        """Search memories by keyword match (rule-based fallback until vector search lands)."""
        # Placeholder implementation
        # In production, would use vector embeddings and similarity search
        if not user_id or not isinstance(user_id, str):
            raise ValueError("user_id must be a non-empty string")
        if not query or not isinstance(query, str):
            raise ValueError("query must be a non-empty string")
        limit = max(1, min(int(limit), 100))
        
        user_memories = self.recall(user_id, limit=100)
        
        # Simple keyword matching as fallback
        query_lower = query.lower()
        results = []
        
        for memory in user_memories:
            content_str = json.dumps(memory['content'], ensure_ascii=False).lower()
            if query_lower in content_str:
                results.append(memory)
        
        return results[:limit]
    
    def get_memory_stats(self, user_id: str) -> Dict[str, Any]:
        """Get statistics about user's memories"""
        user_memory_ids = self.user_indexes.get(user_id, [])
        
        stats = {
            'total_memories': len(user_memory_ids),
            'by_type': {},
            'by_importance': {},
            'total_access_count': 0,
            'oldest_memory': None,
            'newest_memory': None
        }
        
        if not user_memory_ids:
            return stats
        
        # Count by type
        for memory_id in user_memory_ids:
            memory = self.memories[memory_id]
            mem_type = memory.memory_type.value
            stats['by_type'][mem_type] = stats['by_type'].get(mem_type, 0) + 1
            stats['by_importance'][memory.importance.value] = stats['by_importance'].get(memory.importance.value, 0) + 1
            stats['total_access_count'] += memory.access_count
        
        # Find oldest and newest
        sorted_memories = sorted(user_memory_ids, key=lambda mid: self.memories[mid].timestamp)
        if sorted_memories:
            stats['oldest_memory'] = self.memories[sorted_memories[0]].timestamp.isoformat()
            stats['newest_memory'] = self.memories[sorted_memories[-1]].timestamp.isoformat()
        
        return stats
    
    def cleanup_expired(self) -> int:
        """Remove expired memories"""
        current_time = datetime.now(timezone.utc)
        expired_ids = [
            mid for mid, memory in self.memories.items()
            if memory.expires_at and memory.expires_at < current_time
        ]
        
        for memory_id in expired_ids:
            memory = self.memories[memory_id]
            self.forget(memory.user_id, memory_id)
        
        return len(expired_ids)
    
    def export_user_memories(self, user_id: str) -> List[Dict]:
        """Export all memories for a user"""
        return self.recall(user_id, limit=1000)
    
    # Backward compatibility methods for existing code
    def _items(self) -> List[Dict]:
        """Backward compatibility: return all items in old format"""
        return [memory.to_dict() for memory in self.memories.values()]
    
    def remember_legacy(self, subject_id: str, kind: str, content: dict[str, Any]) -> Dict:
        """Backward compatibility: legacy remember method (returns the stored memory dict)."""
        memory_id = self.remember(subject_id, kind, content)
        return self.memories[memory_id].to_dict()

    def recall_legacy(self, subject_id: str, kind: str = None, limit: int = 20) -> list[dict[str, Any]]:
        """Backward compatibility: legacy recall method"""
        # Convert to memory types
        kind_mapping = {
            'conversation': 'conversation',
            'assessment': 'assessment',
            'content_plan': 'content_plan',
            'mistake': 'mistake',
            'preference': 'preference',
            'achievement': 'achievement',
            'question': 'question'
        }

        mapped_type = kind_mapping.get(kind) if kind else None
        return self.recall(subject_id, mapped_type, limit)