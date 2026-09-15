"""
Advanced Security System for Allamni v4.0
Includes encryption, rate limiting, input validation, and security monitoring
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from typing import Dict, List, Optional, Any
from enum import Enum
import secrets
import hashlib
import hmac
import re
import json
from collections import defaultdict

class SecurityLevel(str, Enum):
    """Security levels"""
    BASIC = "basic"
    STANDARD = "standard"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatLevel(str, Enum):
    """Threat levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SecurityConfig:
    """Security configuration"""
    max_failed_attempts: int = 5
    lockout_duration_minutes: int = 30
    password_min_length: int = 8
    password_require_special: bool = True
    password_require_numbers: bool = True
    session_timeout_minutes: int = 30
    rate_limit_requests_per_minute: int = 60
    rate_limit_requests_per_hour: int = 1000
    enable_encryption: bool = True
    enable_audit_logging: bool = True

@dataclass
class RateLimitEntry:
    """Rate limit entry"""
    user_id: str
    endpoint: str
    request_count: int
    window_start: datetime
    window_type: str  # minute, hour, day

@dataclass
class SecurityIncident:
    """Security incident record"""
    id: str
    incident_type: str
    severity: ThreatLevel
    user_id: Optional[str]
    ip_address: str
    description: str
    timestamp: datetime
    resolved: bool = False
    resolution_notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class AdvancedSecurityService:
    """Advanced security service with comprehensive protection"""
    
    def __init__(self, store, config: SecurityConfig = None):
        self.store = store
        self.config = config or SecurityConfig()
        
        # Initialize security collections
        if not hasattr(store, 'rate_limits'):
            store.rate_limits = {}
        if not hasattr(store, 'security_incidents'):
            store.security_incidents = {}
        if not hasattr(store, 'encrypted_data'):
            store.encrypted_data = {}
        if not hasattr(store, 'security_metrics'):
            store.security_metrics = {
                'total_requests': 0,
                'blocked_requests': 0,
                'security_incidents': 0,
                'failed_authentications': 0,  # Not used in this implementation
                'suspicious_activities': 0
            }
    
    def encrypt_data(self, data: str, key: str = None) -> str:
        """Encrypt sensitive data"""
        if not self.config.enable_encryption:
            return data
        
        encryption_key = key or secrets.token_hex(32)
        
        # Simple XOR encryption for demo (in production use AES)
        encrypted = ''.join(chr(ord(c) ^ ord(encryption_key[i % len(encryption_key)])) 
                           for i, c in enumerate(data))
        
        # Store encryption key with the encrypted data
        data_hash = hashlib.sha256(data.encode()).hexdigest()
        self.store.encrypted_data[data_hash] = {
            'encrypted': encrypted,
            'key': encryption_key,  # Store the actual key for decryption
            'key_hash': hashlib.sha256(encryption_key.encode()).hexdigest(),
            'encrypted_at': datetime.now(timezone.utc).isoformat()
        }
        
        return encrypted
    
    def decrypt_data(self, encrypted_data: str, key: str = None) -> str:
        """Decrypt sensitive data"""
        if not self.config.enable_encryption:
            return encrypted_data
        
        # Find the original data in encrypted_data collection
        # Try to find the entry that matches this encrypted data
        for data_hash, entry in self.store.encrypted_data.items():
            if entry['encrypted'] == encrypted_data:
                encryption_key = key or entry.get('key')
                if encryption_key:
                    # Simple XOR decryption (reverse of encryption)
                    decrypted = ''.join(chr(ord(c) ^ ord(encryption_key[i % len(encryption_key)])) 
                                        for i, c in enumerate(encrypted_data))
                    return decrypted
        
        # If no key found, use provided key
        encryption_key = key or secrets.token_hex(32)
        decrypted = ''.join(chr(ord(c) ^ ord(encryption_key[i % len(encryption_key)])) 
                            for i, c in enumerate(encrypted_data))
        
        return decrypted
    
    def check_rate_limit(self, user_id: str, endpoint: str, window_type: str = 'minute') -> bool:
        """Check if request is within rate limits"""
        current_time = datetime.now(timezone.utc)
        
        # Create rate limit key
        key = f"{user_id}_{endpoint}_{window_type}"
        
        # Get or create rate limit entry
        if key not in self.store.rate_limits:
            self.store.rate_limits[key] = RateLimitEntry(
                user_id=user_id,
                endpoint=endpoint,
                request_count=0,
                window_start=current_time,
                window_type=window_type
            )
        
        entry = self.store.rate_limits[key]
        
        # Check if window has expired
        window_duration = {
            'minute': timedelta(minutes=1),
            'hour': timedelta(hours=1),
            'day': timedelta(days=1)
        }.get(window_type, timedelta(minutes=1))
        
        if current_time - entry.window_start > window_duration:
            # Reset window
            entry.request_count = 0
            entry.window_start = current_time
        
        # Get limit based on window type
        limit = {
            'minute': self.config.rate_limit_requests_per_minute,
            'hour': self.config.rate_limit_requests_per_hour,
            'day': self.config.rate_limit_requests_per_hour * 24
        }.get(window_type, self.config.rate_limit_requests_per_minute)
        
        # Check if limit exceeded
        if entry.request_count >= limit:
            self.store.security_metrics['blocked_requests'] = self.store.security_metrics.get('blocked_requests', 0) + 1
            self._report_security_incident(
                incident_type='rate_limit_exceeded',
                severity=ThreatLevel.MEDIUM,
                user_id=user_id,
                description=f'Rate limit exceeded for {endpoint}',
                metadata={'endpoint': endpoint, 'window_type': window_type, 'limit': limit}
            )
            return False
        
        # Increment request count
        entry.request_count += 1
        self.store.security_metrics['total_requests'] = self.store.security_metrics.get('total_requests', 0) + 1
        
        return True
    
    def validate_input(self, input_data: str, input_type: str) -> tuple[bool, Optional[str]]:
        """Validate input data against security rules"""
        if not input_data:
            return True, None
        
        # Check for SQL injection patterns
        sql_patterns = [
            r'(\bunion\b.*\bselect\b)',
            r'(\bselect\b.*\bfrom\b)',
            r'(\binsert\b.*\binto\b)',
            r'(\bdelete\b.*\bfrom\b)',
            r'(\bdrop\b.*\btable\b)',
            r'(--)',
            r'(;)',
            r'(\bor\b.*\b1\b.*\b=)',
            r'(\band\b.*\b1\b.*\b=)'
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, input_data, re.IGNORECASE):
                return False, f"Potential SQL injection detected: {pattern}"
        
        # Check for XSS patterns
        xss_patterns = [
            r'<script',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe',
            r'<object',
            r'<embed'
        ]
        
        for pattern in xss_patterns:
            if re.search(pattern, input_data, re.IGNORECASE):
                return False, f"Potential XSS detected: {pattern}"
        
        # Input type specific validation
        if input_type == 'email':
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, input_data):
                return False, "Invalid email format"
        
        elif input_type == 'password':
            if len(input_data) < self.config.password_min_length:
                return False, f"Password must be at least {self.config.password_min_length} characters"
            
            if self.config.password_require_numbers and not re.search(r'\d', input_data):
                return False, "Password must contain at least one number"
            
            if self.config.password_require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', input_data):
                return False, "Password must contain at least one special character"
        
        elif input_type == 'username':
            if not re.match(r'^[a-zA-Z0-9_]{3,20}$', input_data):
                return False, "Username must be 3-20 alphanumeric characters"
        
        return True, None
    
    def sanitize_input(self, input_data: str) -> str:
        """Sanitize input data"""
        if not input_data:
            return input_data
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', input_data)
        
        # Limit length
        if len(sanitized) > 1000:
            sanitized = sanitized[:1000]
        
        return sanitized
    
    def detect_suspicious_activity(self, user_id: str, activity_type: str, 
                                  metadata: Dict[str, Any] = None) -> bool:
        """Detect suspicious user activity"""
        suspicious = False
        reason = None
        
        # Check for rapid successive actions
        if activity_type == 'login_attempt':
            recent_logins = self._get_recent_user_activity(user_id, 'login_attempt', 
                                                             timedelta(minutes=5))
            if len(recent_logins) > 5:
                suspicious = True
                reason = "Too many login attempts in short time"
        
        # Check for unusual IP addresses
        if activity_type == 'api_request':
            user_ips = self._get_user_ip_addresses(user_id)
            current_ip = metadata.get('ip_address') if metadata else None
            if current_ip and len(user_ips) > 0 and current_ip not in user_ips:
                suspicious = True
                reason = "Login from new IP address"
        
        # Check for unusual time patterns
        if activity_type == 'api_request':
            current_hour = datetime.now(timezone.utc).hour
            if current_hour < 6 or current_hour > 22:  # Unusual hours
                suspicious = True
                reason = "Activity during unusual hours"
        
        if suspicious:
            self.store.security_metrics['suspicious_activities'] = self.store.security_metrics.get('suspicious_activities', 0) + 1
            self._report_security_incident(
                incident_type='suspicious_activity',
                severity=ThreatLevel.MEDIUM,
                user_id=user_id,
                description=reason or "Suspicious activity detected",
                metadata=metadata or {}
            )
        
        return suspicious
    
    def _get_recent_user_activity(self, user_id: str, activity_type: str, 
                                time_window: timedelta) -> List[Dict]:
        """Get recent user activity"""
        # This would query from a proper activity log in production
        # For demo, return empty list
        return []
    
    def _get_user_ip_addresses(self, user_id: str) -> set:
        """Get set of IP addresses used by user"""
        # This would query from proper log in production
        # For demo, return empty set
        return set()
    
    def _report_security_incident(self, incident_type: str, severity: ThreatLevel,
                                user_id: Optional[str], description: str, 
                                metadata: Dict[str, Any]):
        """Report security incident"""
        incident = SecurityIncident(
            id=str(uuid4()),
            incident_type=incident_type,
            severity=severity,
            user_id=user_id,
            ip_address=metadata.get('ip_address', 'unknown'),
            description=description,
            timestamp=datetime.now(timezone.utc),
            metadata=metadata
        )
        
        self.store.security_incidents[incident.id] = incident
        self.store.security_metrics['security_incidents'] = self.store.security_metrics.get('security_incidents', 0) + 1
    
    def get_security_metrics(self) -> Dict[str, Any]:
        """Get security metrics"""
        return self.store.security_metrics.copy()
    
    def get_recent_incidents(self, limit: int = 50) -> List[Dict]:
        """Get recent security incidents"""
        incidents = []
        for incident in self.store.security_incidents.values():
            incidents.append({
                'id': incident.id,
                'incident_type': incident.incident_type,
                'severity': incident.severity.value,
                'user_id': incident.user_id,
                'description': incident.description,
                'timestamp': incident.timestamp.isoformat(),
                'resolved': incident.resolved
            })
        
        # Sort by timestamp descending
        incidents.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return incidents[:limit]
    
    def resolve_incident(self, incident_id: str, resolution_notes: str) -> bool:
        """Resolve a security incident"""
        incident = self.store.security_incidents.get(incident_id)
        if not incident:
            return False
        
        incident.resolved = True
        incident.resolution_notes = resolution_notes
        
        return True
    
    def perform_security_scan(self) -> Dict[str, Any]:
        """Perform comprehensive security scan"""
        scan_results = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'security_score': 100,
            'issues': [],
            'recommendations': []
        }
        
        # Check for suspicious activities
        suspicious_count = self.store.security_metrics.get('suspicious_activities', 0)
        if suspicious_count > 10:
            scan_results['security_score'] -= 20
            scan_results['issues'].append(f"High suspicious activity count: {suspicious_count}")
            scan_results['recommendations'].append("Review user activity logs")
        
        # Check for rate limit violations
        blocked_count = self.store.security_metrics.get('blocked_requests', 0)
        if blocked_count > 50:
            scan_results['security_score'] -= 15
            scan_results['issues'].append(f"High rate limit violations: {blocked_count}")
            scan_results['recommendations'].append("Implement stricter rate limiting")
        
        # Check for unresolved incidents
        unresolved_incidents = len([i for i in self.store.security_incidents.values() 
                                   if not i.resolved])
        if unresolved_incidents > 5:
            scan_results['security_score'] -= 10
            scan_results['issues'].append(f"Unresolved security incidents: {unresolved_incidents}")
            scan_results['recommendations'].append("Review and resolve security incidents")
        
        return scan_results

# Factory function
def get_advanced_security_service(store, config: SecurityConfig = None) -> AdvancedSecurityService:
    """Get or create advanced security service instance"""
    if not hasattr(store, 'advanced_security_service') or store.advanced_security_service is None:
        store.advanced_security_service = AdvancedSecurityService(store, config)
    return store.advanced_security_service