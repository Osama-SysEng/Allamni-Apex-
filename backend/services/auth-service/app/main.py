from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4
from shared.config.settings import settings
from shared.identity import active_session, create_session, record_consent, revoke_session, rotate_refresh
from shared.security import create_token, decode_token
from shared.store import store
import hashlib, os, hmac

app = FastAPI(title='Allamni Auth Service')
CONSENT_PURPOSE = 'personalized_learning'
CONSENT_VERSION = '2026-08'


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)
    full_name: str
    role: str = 'student'
    goal_domain: str = 'general'


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=20)


class ConsentRequest(BaseModel):
    granted: bool
    version: str = CONSENT_VERSION


def hash_password(password):
    salt = os.urandom(16)
    return salt.hex() + '$' + hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 210000).hex()


def verify(password, stored):
    salt, digest = stored.split('$')
    candidate = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), 210000).hex()
    return hmac.compare_digest(candidate, digest)


def token_pair(user: dict, session: dict) -> dict:
    return {
        'access_token': create_token(user['id'], user['role'], 'access', session['id']),
        'refresh_token': create_token(user['id'], user['role'], 'refresh', session['id'], session['refresh_jti']),
        'token_type': 'bearer',
        'expires_in': settings.jwt_access_minutes * 60,
        'session_id': session['id'],
        'user': {'id': user['id'], 'email': user['email'], 'full_name': user['full_name'], 'role': user['role']},
    }


def current(authorization: str) -> dict:
    if not authorization.startswith('Bearer '):
        raise HTTPException(401, 'missing bearer token')
    try:
        claims = decode_token(authorization[7:])
    except Exception as exc:
        raise HTTPException(401, 'invalid token') from exc
    if claims.get('type') != 'access' or not active_session(claims.get('sid'), claims.get('sub')):
        raise HTTPException(401, 'session is not active')
    return claims


@app.get('/health')
def health(): return {'status': 'ok', 'service': 'auth'}


@app.post('/register')
def register(body: RegisterRequest):
    body.email = body.email.strip().lower()
    if body.role not in {'student', 'admin', 'institution_manager'}: raise HTTPException(400, 'invalid role')
    if body.email in store.users_by_email: raise HTTPException(409, 'email already registered')
    user_id = str(uuid4())
    user = {'id': user_id, 'email': body.email, 'full_name': body.full_name, 'role': body.role, 'password_hash': hash_password(body.password), 'active': True}
    store.users[user_id] = user; store.users_by_email[body.email] = user
    if body.role == 'student':
        from shared.models import LearningProfile, Skill, LearningPreferences
        store.profiles[user_id] = LearningProfile(student_id=user_id, goal_domain=body.goal_domain, learning_preferences=LearningPreferences(content_format=['video', 'interactive']), skills=[Skill(code='python_basics', name='أساسيات البرمجة', level=.35, target=.75, confidence=.55, importance=1), Skill(code='oop', name='البرمجة الكائنية', level=.22, target=.70, confidence=.48, importance=.9), Skill(code='problem_solving', name='حل المشكلات', level=.40, target=.80, confidence=.60, importance=.95), Skill(code='data_structures', name='هياكل البيانات', level=.15, target=.65, confidence=.35, importance=.85)])
    response = token_pair(user, create_session(user_id, body.role, settings.jwt_refresh_days))
    response['consent_required'] = body.role == 'student'
    return response


@app.post('/login')
def login(body: LoginRequest):
    user = store.users_by_email.get(body.email.strip().lower())
    if not user or not user.get('active', True) or not verify(body.password, user['password_hash']): raise HTTPException(401, 'invalid credentials')
    response = token_pair(user, create_session(user['id'], user['role'], settings.jwt_refresh_days))
    response['consent_required'] = user['role'] == 'student' and not store.consents.get((user['id'], CONSENT_PURPOSE), {}).get('granted')
    return response


@app.post('/refresh')
def refresh(body: RefreshRequest):
    try: claims = decode_token(body.refresh_token)
    except Exception as exc: raise HTTPException(401, 'invalid refresh token') from exc
    if claims.get('type') != 'refresh': raise HTTPException(401, 'invalid refresh token')
    session = rotate_refresh(claims.get('sid'), claims.get('jti'))
    user = store.users.get(claims.get('sub'))
    if not session or not user: raise HTTPException(401, 'refresh session is not active')
    return token_pair(user, session)


@app.post('/logout', status_code=204)
def logout(authorization: str = Header('')):
    claims = current(authorization)
    revoke_session(claims['sid'], 'user_logout', claims['sub'])


@app.post('/me/consent')
def consent(body: ConsentRequest, authorization: str = Header('')):
    claims = current(authorization)
    if claims['role'] != 'student': raise HTTPException(403, 'student role required')
    return record_consent(claims['sub'], CONSENT_PURPOSE, body.granted, body.version)
