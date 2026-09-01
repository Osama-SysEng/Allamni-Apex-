from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from shared.config.settings import settings
from shared.identity import active_session, audit
from shared.security import decode_token
from shared.store import store

app = FastAPI(title='Allamni Integration Service')


class SyncEvent(BaseModel):
    event_type: str = Field(min_length=3, max_length=120)
    payload: dict
    idempotency_key: str = Field(min_length=8, max_length=100)


def admin(authorization):
    if not authorization.startswith('Bearer '): raise HTTPException(401, 'missing token')
    try: c = decode_token(authorization[7:])
    except Exception as exc: raise HTTPException(401, 'invalid token') from exc
    if c.get('type') != 'access' or not active_session(c.get('sid'), c.get('sub')): raise HTTPException(401, 'inactive session')
    if c['role'] not in {'admin', 'institution_manager'}: raise HTTPException(403, 'admin role required')
    return c


@app.get('/health')
def health(): return {'status': 'ok', 'service': 'integration'}


@app.post('/odoo/queue')
def queue(body: SyncEvent, authorization: str = Header('')):
    claims = admin(authorization)
    existing = next((item for item in store.outbox if item['idempotency_key'] == body.idempotency_key), None)
    if existing: return {**existing, 'idempotent_replay': True}
    item = {'id': str(uuid4()), 'event_type': body.event_type, 'payload': body.payload, 'idempotency_key': body.idempotency_key, 'status': 'PENDING', 'attempts': 0, 'last_error': None}
    store.outbox.append(item)
    audit(claims['sub'], 'INTEGRATION_EVENT_QUEUED', 'Outbox', item['id'], {'event_type': body.event_type})
    return {**item, 'idempotent_replay': False}


@app.post('/odoo/sync')
def sync(authorization: str = Header('')):
    claims = admin(authorization)
    if not settings.odoo_url:
        blocked = 0
        for item in store.outbox:
            if item['status'] in {'PENDING', 'RETRY'}:
                item['status'] = 'BLOCKED'; item['last_error'] = 'Odoo integration is not configured'; blocked += 1
        audit(claims['sub'], 'INTEGRATION_SYNC_BLOCKED', 'Outbox', details={'blocked': blocked})
        return {'synced': 0, 'blocked': blocked, 'message': 'Configure ODOO_URL and credentials before delivery'}
    # Actual RPC is intentionally not performed here: it requires an approved adapter and staging credentials.
    candidates = [item for item in store.outbox if item['status'] in {'PENDING', 'RETRY'}]
    for item in candidates:
        item['attempts'] += 1; item['status'] = 'RETRY'; item['last_error'] = 'Adapter not enabled in this release'
    audit(claims['sub'], 'INTEGRATION_SYNC_DEFERRED', 'Outbox', details={'retry': len(candidates)})
    return {'synced': 0, 'retry': len(candidates), 'message': 'Adapter requires approved staging credentials'}


@app.get('/odoo/status')
def status(authorization: str = Header('')):
    admin(authorization)
    counts = {state: len([item for item in store.outbox if item['status'] == state]) for state in {'PENDING', 'RETRY', 'BLOCKED', 'DEAD_LETTER'}}
    return {'configured': bool(settings.odoo_url), 'counts': counts, 'message': 'No remote sync is executed without a configured adapter and approved credentials.'}
