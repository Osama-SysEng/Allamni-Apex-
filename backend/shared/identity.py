"""Session lifecycle and learner-consent controls for service runtimes."""
import time
from uuid import uuid4

from shared.store import store


def audit(actor_id: str | None, action: str, entity_type: str, entity_id: str | None = None, details: dict | None = None) -> dict:
    event = {'id': str(uuid4()), 'actor_id': actor_id, 'action': action, 'entity_type': entity_type, 'entity_id': entity_id, 'details': details or {}, 'at': int(time.time())}
    store.audit.append(event)
    return event


def create_session(user_id: str, role: str, refresh_days: int) -> dict:
    session = {'id': str(uuid4()), 'user_id': user_id, 'role': role, 'refresh_jti': str(uuid4()), 'expires_at': int(time.time()) + refresh_days * 86400, 'revoked_at': None, 'revoke_reason': None}
    store.sessions[session['id']] = session
    audit(user_id, 'AUTH_SESSION_CREATED', 'Session', session['id'])
    return session


def active_session(session_id: str | None, user_id: str | None = None) -> dict | None:
    session = store.sessions.get(session_id or '')
    if not session or session['revoked_at'] or session['expires_at'] <= time.time():
        return None
    if user_id and session['user_id'] != user_id:
        return None
    return session


def revoke_session(session_id: str, reason: str, actor_id: str | None = None) -> bool:
    session = store.sessions.get(session_id)
    if not session or session['revoked_at']:
        return False
    session['revoked_at'] = int(time.time())
    session['revoke_reason'] = reason
    audit(actor_id or session['user_id'], 'AUTH_SESSION_REVOKED', 'Session', session_id, {'reason': reason})
    return True


def rotate_refresh(session_id: str, supplied_jti: str) -> dict | None:
    session = active_session(session_id)
    if not session:
        return None
    if session['refresh_jti'] != supplied_jti:
        revoke_session(session_id, 'refresh_replay_detected')
        audit(session['user_id'], 'AUTH_SESSION_REPLAY_BLOCKED', 'Session', session_id)
        return None
    session['refresh_jti'] = str(uuid4())
    audit(session['user_id'], 'AUTH_SESSION_REFRESHED', 'Session', session_id)
    return session


def record_consent(user_id: str, purpose: str, granted: bool, version: str) -> dict:
    record = {'user_id': user_id, 'purpose': purpose, 'granted': granted, 'version': version, 'updated_at': int(time.time())}
    store.consents[(user_id, purpose)] = record
    audit(user_id, 'LEARNER_CONSENT_UPDATED', 'Consent', purpose, {'granted': granted, 'version': version})
    return record


def has_consent(user_id: str, purpose: str) -> bool:
    return bool(store.consents.get((user_id, purpose), {}).get('granted'))
