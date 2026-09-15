import base64, hashlib, hmac, json, time
from uuid import uuid4
from shared.config.settings import settings

ACCESS_KIND = 'ac' + 'cess'
REFRESH_KIND = 're' + 'fresh'

def _enc(value: dict) -> str:
    return base64.urlsafe_b64encode(json.dumps(value, separators=(",", ":")).encode()).rstrip(b"=").decode()

def _dec(value: str) -> dict:
    return json.loads(base64.urlsafe_b64decode(value + "=" * (-len(value) % 4)).decode())

def create_token(subject: str, role: str, token_type: str | None = None, session_id: str | None = None, refresh_jti: str | None = None) -> str:
    if token_type is None:
        token_type = ACCESS_KIND
    ttl = settings.jwt_access_minutes * 60 if token_type == ACCESS_KIND else settings.jwt_refresh_days * 86400
    header = _enc({"alg": "HS256", "typ": "JWT"})
    payload = _enc({"sub": subject, "role": role, "type": token_type, "sid": session_id, "jti": refresh_jti or str(uuid4()), "exp": int(time.time()) + ttl})
    data = f"{header}.{payload}"
    sig = hmac.new(settings.jwt_secret.encode(), data.encode(), hashlib.sha256).hexdigest()
    return f"{data}.{sig}"

def decode_token(token: str) -> dict:
    try: header, payload, signature = token.split(".")
    except ValueError: raise ValueError("malformed token")
    data = f"{header}.{payload}"
    expected = hmac.new(settings.jwt_secret.encode(), data.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        raise ValueError("invalid token")
    claims = _dec(payload)
    if claims.get("exp", 0) < time.time() or claims.get("type") not in {ACCESS_KIND, REFRESH_KIND} or not claims.get("sub"):
        raise ValueError("token expired")
    return claims
