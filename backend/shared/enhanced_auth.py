"""
Enhanced Authentication System for Allamni v4.0
Supports 2FA, biometric authentication, session management, and security features
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from typing import Dict, List, Optional, Any
from enum import Enum
import secrets
import hashlib
import hmac
import json

class AuthMethod(str, Enum):
    """Authentication methods"""
    PASSWORD = "password"
    CODE = "code"
    BIOMETRIC = "biometric"
    SSO = "sso"
    OAUTH = "oauth"

class AuthStatus(str, Enum):
    """Authentication status"""
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    LOCKED = "locked"
    EXPIRED = "expired"

class SecurityLevel(str, Enum):
    """Security levels"""
    BASIC = "basic"
    STANDARD = "standard"
    HIGH = "high"
    MAXIMUM = "maximum"

@dataclass
class AuthSession:
    """User authentication session"""
    id: str
    user_id: str
    token: str
    refresh_token: str
    expires_at: datetime
    created_at: datetime
    last_activity: datetime
    ip_address: str
    user_agent: str
    device_id: str
    is_active: bool = True
    revoked_at: Optional[datetime] = None
    revoked_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Check if session is expired"""
        return datetime.now(timezone.utc) > self.expires_at
    
    def is_valid(self) -> bool:
        """Check if session is valid"""
        return self.is_active and not self.is_expired() and self.revoked_at is None

@dataclass
class TwoFactorAuth:
    """Two-factor authentication configuration"""
    user_id: str
    secret: str
    backup_codes: List[str]
    is_enabled: bool
    verified_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    recovery_code: Optional[str] = None
    
    def generate_backup_codes(self, count: int = 10) -> List[str]:
        """Generate backup codes for 2FA recovery"""
        self.backup_codes = [secrets.token_hex(16).upper() for _ in range(count)]
        return self.backup_codes
    
    def verify_backup_code(self, code: str) -> bool:
        """Verify backup code and remove it if valid"""
        if code in self.backup_codes:
            self.backup_codes.remove(code)
            return True
        return False

@dataclass
class BiometricAuth:
    """Biometric authentication data"""
    user_id: str
    device_id: str
    biometric_hash: str
    enabled_at: datetime
    last_used: Optional[datetime] = None
    is_enabled: bool = True
    
    def verify_biometric(self, provided_hash: str) -> bool:
        """Verify biometric data"""
        return hmac.compare_digest(self.biometric_hash, provided_hash)

@dataclass
class SecurityEvent:
    """Security-related events for audit logging"""
    id: str
    user_id: str
    event_type: str
    description: str
    ip_address: str
    user_agent: str
    timestamp: datetime
    severity: str  # low, medium, high, critical
    metadata: Dict[str, Any] = field(default_factory=dict)

class EnhancedAuthService:
    """Enhanced authentication service with advanced security features"""
    
    def __init__(self, store):
        self.store = store
        # Initialize security collections if not exist
        if not hasattr(store, 'auth_sessions'):
            store.auth_sessions = {}
        if not hasattr(store, 'two_factor_auths'):
            store.two_factor_auths = {}
        if not hasattr(store, 'biometric_auths'):
            store.biometric_auths = {}
        if not hasattr(store, 'security_events'):
            store.security_events = {}
        if not hasattr(store, 'failed_login_attempts'):
            store.failed_login_attempts = {}
        if not hasattr(store, 'account_lockouts'):
            store.account_lockouts = {}
        
        # Security settings
        self.max_failed_attempts = 5
        self.lockout_duration = timedelta(minutes=30)
        self.session_duration = timedelta(hours=24)
        self.inactivity_timeout = timedelta(minutes=30)
    
    def create_session(self, user_id: str, ip_address: str, user_agent: str, 
                       device_id: str, security_level: SecurityLevel = SecurityLevel.STANDARD) -> AuthSession:
        """Create new authentication session"""
        session_id = str(uuid4())
        token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32)
        
        # Set session duration based on security level
        if security_level == SecurityLevel.MAXIMUM:
            duration = timedelta(hours=1)
        elif security_level == SecurityLevel.HIGH:
            duration = timedelta(hours=8)
        else:
            duration = self.session_duration
        
        session = AuthSession(
            id=session_id,
            user_id=user_id,
            token=token,
            refresh_token=refresh_token,
            expires_at=datetime.now(timezone.utc) + duration,
            created_at=datetime.now(timezone.utc),
            last_activity=datetime.now(timezone.utc),
            ip_address=ip_address,
            user_agent=user_agent,
            device_id=device_id,
            metadata={'security_level': security_level.value}
        )
        
        self.store.auth_sessions[session_id] = session
        
        # Log security event
        self._log_security_event(
            user_id=user_id,
            event_type='session_created',
            description='New authentication session created',
            ip_address=ip_address,
            user_agent=user_agent,
            severity='low'
        )
        
        return session
    
    def validate_session(self, session_id: str, ip_address: str, user_agent: str) -> bool:
        """Validate session and update activity"""
        session = self.store.auth_sessions.get(session_id)
        if not session:
            return False
        
        if not session.is_valid():
            return False
        
        # Check for IP address changes (security measure)
        if session.ip_address != ip_address:
            self._log_security_event(
                user_id=session.user_id,
                event_type='ip_address_changed',
                description=f'Session IP changed from {session.ip_address} to {ip_address}',
                ip_address=ip_address,
                user_agent=user_agent,
                severity='medium'
            )
        
        # Update last activity
        session.last_activity = datetime.now(timezone.utc)
        
        return True
    
    def revoke_session(self, session_id: str, reason: str) -> bool:
        """Revoke a session"""
        session = self.store.auth_sessions.get(session_id)
        if not session:
            return False
        
        session.is_active = False
        session.revoked_at = datetime.now(timezone.utc)
        session.revoked_reason = reason
        
        self._log_security_event(
            user_id=session.user_id,
            event_type='session_revoked',
            description=f'Session revoked: {reason}',
            ip_address=session.ip_address,
            user_agent=session.user_agent,
            severity='medium'
        )
        
        return True
    
    def revoke_all_user_sessions(self, user_id: str, reason: str) -> int:
        """Revoke all sessions for a user"""
        count = 0
        for session_id, session in self.store.auth_sessions.items():
            if session.user_id == user_id and session.is_active:
                self.revoke_session(session_id, reason)
                count += 1
        return count
    
    def setup_2fa(self, user_id: str) -> TwoFactorAuth:
        """Setup two-factor authentication for user"""
        # Generate secret (using standard library fallback)
        secret = secrets.token_hex(32).upper()
        
        # Generate backup codes
        backup_codes = [secrets.token_hex(16).upper() for _ in range(10)]
        
        two_fa = TwoFactorAuth(
            user_id=user_id,
            secret=secret,
            backup_codes=backup_codes,
            is_enabled=False
        )
        
        self.store.two_factor_auths[user_id] = two_fa
        
        self._log_security_event(
            user_id=user_id,
            event_type='2fa_setup',
            description='2FA setup initiated',
            ip_address='system',
            user_agent='system',
            severity='low'
        )
        
        return two_fa
    
    def enable_2fa(self, user_id: str, verification_code: str) -> bool:
        """Enable 2FA after verification"""
        two_fa = self.store.two_factor_auths.get(user_id)
        if not two_fa:
            return False
        
        # Verify the code using simple time-based validation
        if self._verify_2fa_code(two_fa, verification_code):
            two_fa.is_enabled = True
            two_fa.verified_at = datetime.now(timezone.utc)
            
            self._log_security_event(
                user_id=user_id,
                event_type='2fa_enabled',
                description='2FA successfully enabled',
                ip_address='system',
                user_agent='system',
                severity='low'
            )
            
            return True
        
        return False
    
    def _verify_2fa_code(self, two_fa: TwoFactorAuth, code: str) -> bool:
        """Verify 2FA code using time-based validation (simplified)"""
        # Simplified 2FA verification - in production would use proper TOTP
        # For demo, we check if code matches secret or backup codes
        current_time = int(datetime.now(timezone.utc).timestamp())
        time_window = current_time // 30  # 30-second windows
        
        # Generate expected code based on time window
        expected_code = hashlib.sha256(f"{two_fa.secret}{time_window}".encode()).hexdigest()[:6].upper()
        
        if code == expected_code:
            return True
        
        # Check backup codes
        if code in two_fa.backup_codes:
            two_fa.backup_codes.remove(code)
            return True
        
        return False
    
    def verify_2fa(self, user_id: str, code: str) -> bool:
        """Verify 2FA code"""
        two_fa = self.store.two_factor_auths.get(user_id)
        if not two_fa or not two_fa.is_enabled:
            return False
        
        if self._verify_2fa_code(two_fa, code):
            two_fa.last_used = datetime.now(timezone.utc)
            return True
        
        return False
    
    def setup_biometric(self, user_id: str, device_id: str, biometric_data: str) -> BiometricAuth:
        """Setup biometric authentication"""
        # Hash biometric data for security
        biometric_hash = hashlib.sha256(biometric_data.encode()).hexdigest()
        
        biometric = BiometricAuth(
            user_id=user_id,
            device_id=device_id,
            biometric_hash=biometric_hash,
            enabled_at=datetime.now(timezone.utc),
            is_enabled=True
        )
        
        # Store by user_device key
        key = f"{user_id}_{device_id}"
        self.store.biometric_auths[key] = biometric
        
        self._log_security_event(
            user_id=user_id,
            event_type='biometric_setup',
            description=f'Biometric auth setup for device {device_id}',
            ip_address='system',
            user_agent='system',
            severity='low'
        )
        
        return biometric
    
    def verify_biometric(self, user_id: str, device_id: str, provided_biometric: str) -> bool:
        """Verify biometric authentication"""
        key = f"{user_id}_{device_id}"
        biometric = self.store.biometric_auths.get(key)
        
        if not biometric or not biometric.is_enabled:
            return False
        
        provided_hash = hashlib.sha256(provided_biometric.encode()).hexdigest()
        
        if biometric.verify_biometric(provided_hash):
            biometric.last_used = datetime.now(timezone.utc)
            return True
        
        return False
    
    def record_failed_login(self, user_id: str, ip_address: str) -> int:
        """Record failed login attempt"""
        attempts = self.store.failed_login_attempts.get(user_id, 0) + 1
        self.store.failed_login_attempts[user_id] = attempts
        
        # Check if account should be locked
        if attempts >= self.max_failed_attempts:
            self._lock_account(user_id, ip_address)
        
        self._log_security_event(
            user_id=user_id,
            event_type='failed_login',
            description=f'Failed login attempt {attempts}/{self.max_failed_attempts}',
            ip_address=ip_address,
            user_agent='unknown',
            severity='high' if attempts >= self.max_failed_attempts - 1 else 'medium'
        )
        
        return attempts
    
    def _lock_account(self, user_id: str, ip_address: str):
        """Lock account due to too many failed attempts"""
        lockout_until = datetime.now(timezone.utc) + self.lockout_duration
        
        self.store.account_lockouts[user_id] = {
            'locked_at': datetime.now(timezone.utc).isoformat(),
            'locked_until': lockout_until.isoformat(),
            'ip_address': ip_address,
            'reason': 'Too many failed login attempts'
        }
        
        self._log_security_event(
            user_id=user_id,
            event_type='account_locked',
            description='Account locked due to too many failed login attempts',
            ip_address=ip_address,
            user_agent='unknown',
            severity='critical'
        )
    
    def is_account_locked(self, user_id: str) -> bool:
        """Check if account is locked"""
        lockout = self.store.account_lockouts.get(user_id)
        if not lockout:
            return False
        
        locked_until = datetime.fromisoformat(lockout['locked_until'])
        if datetime.now(timezone.utc) > locked_until:
            # Lockout expired, remove it
            del self.store.account_lockouts[user_id]
            return False
        
        return True
    
    def get_remaining_lockout_time(self, user_id: str) -> Optional[timedelta]:
        """Get remaining lockout time"""
        lockout = self.store.account_lockouts.get(user_id)
        if not lockout:
            return None
        
        locked_until = datetime.fromisoformat(lockout['locked_until'])
        remaining = locked_until - datetime.now(timezone.utc)
        
        return remaining if remaining.total_seconds() > 0 else None
    
    def reset_failed_attempts(self, user_id: str):
        """Reset failed login attempts after successful login"""
        if user_id in self.store.failed_login_attempts:
            del self.store.failed_login_attempts[user_id]
    
    def _log_security_event(self, user_id: str, event_type: str, description: str, 
                           ip_address: str, user_agent: str, severity: str):
        """Log security event for audit"""
        event = SecurityEvent(
            id=str(uuid4()),
            user_id=user_id,
            event_type=event_type,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.now(timezone.utc),
            severity=severity
        )
        
        self.store.security_events[event.id] = event
    
    def get_security_events(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get security events for a user"""
        events = []
        for event in self.store.security_events.values():
            if event.user_id == user_id:
                events.append({
                    'id': event.id,
                    'event_type': event.event_type,
                    'description': event.description,
                    'timestamp': event.timestamp.isoformat(),
                    'severity': event.severity,
                    'ip_address': event.ip_address
                })
        
        # Sort by timestamp descending
        events.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return events[:limit]
    
    def get_active_sessions(self, user_id: str) -> List[Dict]:
        """Get all active sessions for a user"""
        sessions = []
        for session in self.store.auth_sessions.values():
            if session.user_id == user_id and session.is_active and session.is_valid():
                sessions.append({
                    'id': session.id,
                    'device_id': session.device_id,
                    'ip_address': session.ip_address,
                    'created_at': session.created_at.isoformat(),
                    'last_activity': session.last_activity.isoformat(),
                    'expires_at': session.expires_at.isoformat()
                })
        
        return sessions
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions"""
        count = 0
        for session_id, session in list(self.store.auth_sessions.items()):
            if session.is_expired():
                session.is_active = False
                session.revoked_at = datetime.now(timezone.utc)
                session.revoked_reason = 'expired'
                count += 1
        
        return count

# Factory function
def get_enhanced_auth_service(store) -> EnhancedAuthService:
    """Get or create enhanced auth service instance"""
    if not hasattr(store, 'enhanced_auth_service') or store.enhanced_auth_service is None:
        store.enhanced_auth_service = EnhancedAuthService(store)
    return store.enhanced_auth_service