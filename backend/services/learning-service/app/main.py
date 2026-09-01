import time, uuid

from fastapi import FastAPI, Header, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from shared.security import decode_token
from shared.identity import active_session, has_consent, record_consent, audit
from shared.store import store
from shared.models import Resource, LearningProfile, Skill
from shared.engines import build_roadmap, recommend_next_action, score_assessment, update_mastery
from shared.analytics import overview
from shared.intelligence import AgentOrchestrator, cognitive_snapshot, risk_score, AssessmentAgent, adaptive_difficulty
from shared.content import lesson_blueprint
from shared.events import EventBus
from shared.policy import authorize_action
from shared.metrics import metrics
from shared.operational import http_metrics

app=FastAPI(title="Allamni Learning Intelligence Service", version="3.0.0")
bus=EventBus(store); orchestrator=AgentOrchestrator()

@app.middleware('http')
async def operational_controls(request: Request, call_next):
    started = time.perf_counter(); correlation = request.headers.get('X-Request-Id') or uuid.uuid4().hex; http_metrics.started()
    try:
        response = await call_next(request)
        response.headers['X-Request-Id'] = correlation
        http_metrics.record(getattr(request.scope.get('route'), 'path', request.url.path), response.status_code, time.perf_counter() - started)
        return response
    except Exception:
        http_metrics.record(request.url.path, 500, time.perf_counter() - started)
        raise
    finally: http_metrics.completed()


def current(authorization:str=Header("")):
    if not authorization.startswith("Bearer "): raise HTTPException(401,"missing bearer token")
    try:
        claims = decode_token(authorization[7:])
        if claims.get('type') != 'access' or not active_session(claims.get('sid'), claims.get('sub')): raise ValueError('session inactive')
        return claims
    except Exception as e: raise HTTPException(401,str(e))

class ResourceCreate(BaseModel):
    title:str; platform:str; url:str; skills:list[str]=[]; attributes:list[str]=[]
    duration_minutes:int|None=None; quality_score:float=Field(.5,ge=0,le=1)

class AssessmentSubmit(BaseModel):
    responses:list[dict]
    difficulty: float = Field(.5, ge=.05, le=.95)
    idempotency_key: str = Field(min_length=8, max_length=100)

class ContentReq(BaseModel):
    skill_code:str; age_band:str="all"; language:str="ar"; formats:list[str]=["mind_map","interactive_game","video","image"]

class ConsentReq(BaseModel):
    granted: bool
    version: str = '2026-08'

def personalized(c: dict):
    if c.get('role') != 'student': raise HTTPException(403, 'student role required')
    if not has_consent(c['sub'], 'personalized_learning'): raise HTTPException(403, 'personalized learning consent required')

@app.get("/health")
def health(): return {"status":"ok","service":"learning","version":"3.0.0"}

@app.get("/metrics")
def metrics_endpoint(c=Depends(current)):
    if c.get('role') not in {'admin', 'institution_manager'}: raise HTTPException(403, 'institution role required')
    return {'learning': metrics.snapshot(), 'http': http_metrics.snapshot()}

@app.get('/ready')
def ready():
    return {'status': 'ready', 'state_backend': 'memory-development-adapter', 'production_requirement': 'managed PostgreSQL migration and repository adapter'}

@app.get("/students/me")
def me(c=Depends(current)):
    profile=store.profiles.get(c["sub"])
    if not profile: raise HTTPException(404,"student profile not found")
    metrics.inc("profile_reads")
    return {"profile":profile.model_dump(),"cognitive":cognitive_snapshot(profile),"risk":risk_score(profile),"roadmap":build_roadmap(profile)}

@app.get("/students/me/intelligence")
def intelligence(c=Depends(current)):
    personalized(c)
    profile=store.profiles.get(c["sub"])
    if not profile: raise HTTPException(404,"student profile not found")
    trace=orchestrator.run(profile)
    store.memory.remember(c["sub"],"agent_trace",trace)
    return {"cognitive":cognitive_snapshot(profile),"risk":risk_score(profile),"orchestration":trace,"memory":store.memory.recall(c["sub"],limit=10)}

@app.get("/students/me/next-best-action")
def next_action(c=Depends(current)):
    personalized(c)
    profile=store.profiles.get(c["sub"])
    if not profile: raise HTTPException(404,"student profile not found")
    result=recommend_next_action(profile,store.resources).model_dump()
    result["risk"]=risk_score(profile); result["cognitive"]=cognitive_snapshot(profile)
    return result

@app.get("/students/me/lesson-blueprint")
def lesson(c=Depends(current)):
    personalized(c)
    profile=store.profiles.get(c["sub"])
    if not profile: raise HTTPException(404,"student profile not found")
    return lesson_blueprint(profile,store.resources)

@app.post("/students/me/assessments/submit")
def submit_assessment(body:AssessmentSubmit,c=Depends(current)):
    personalized(c)
    profile=store.profiles.get(c["sub"])
    if not profile: raise HTTPException(404,"student profile not found")
    prior = store.assessment_attempts.get((c['sub'], body.idempotency_key))
    if prior: return {**prior, 'idempotent_replay': True}
    result=score_assessment(body.responses)
    for item in body.responses:
        skill_code=item.get("skill_code")
        if skill_code:
            for skill in profile.skills:
                if skill.code==skill_code:
                    skill.level,skill.confidence=update_mastery(skill.level,skill.confidence,float(item.get("score",0)))
    next_diff=adaptive_difficulty(body.difficulty,result["score"],cognitive_snapshot(profile)["confidence"])
    event=bus.publish("assessment.completed",c["sub"],{"result":result,"next_difficulty":next_diff})
    store.memory.remember(c["sub"],"assessment",{"result":result,"next_difficulty":next_diff})
    metrics.inc("assessment_completed")
    response = {"result":result,"next_difficulty":next_diff,"event_id":event["id"],"roadmap":build_roadmap(profile),"risk":risk_score(profile), 'idempotent_replay': False}
    store.assessment_attempts[(c['sub'], body.idempotency_key)] = response
    audit(c['sub'], 'ASSESSMENT_COMPLETED', 'AssessmentAttempt', body.idempotency_key, {'score': result['score']})
    return response

@app.post("/students/me/content/plan")
def content_plan(body:ContentReq,c=Depends(current)):
    personalized(c)
    profile=store.profiles.get(c["sub"])
    if not profile: raise HTTPException(404,"student profile not found")
    if body.skill_code not in {s.code for s in profile.skills}: raise HTTPException(400,"skill not in profile")
    blueprint=lesson_blueprint(profile,store.resources); blueprint["requested_formats"]=body.formats; blueprint["age_band"]=body.age_band; blueprint["language"]=body.language
    store.memory.remember(c["sub"],"content_plan",blueprint)
    return blueprint

@app.get("/students/me/memory")
def memory(c=Depends(current)):
    personalized(c)
    return {"items":store.memory.recall(c["sub"],limit=50)}

@app.post('/students/me/consent')
def consent(body: ConsentReq, c=Depends(current)):
    if c.get('role') != 'student': raise HTTPException(403, 'student role required')
    return record_consent(c['sub'], 'personalized_learning', body.granted, body.version)


@app.get("/institution/intelligence")
def institution_intelligence(c=Depends(current)):
    if c["role"] not in {"admin","institution_manager"}: raise HTTPException(403,"institution role required")
    rows=[]
    for sid, profile in store.profiles.items():
        if not has_consent(sid, 'personalized_learning'): continue
        rows.append({"student_id":sid,"cognitive":cognitive_snapshot(profile),"risk":risk_score(profile)})
    high=[r for r in rows if r["risk"]["level"] in {"high","critical"}]
    return {"students":len(rows),"high_risk":len(high),"risk_rate":round(len(high)/max(1,len(rows)),4)}

@app.post("/admin/resources")
def add_resource(body:ResourceCreate,c=Depends(current)):
    decision=authorize_action(c["role"],"create_resource",None,c["sub"])
    if not decision["allowed"]: raise HTTPException(403,"admin role required")
    resource=Resource(id=f"res_{len(store.resources)+1}",**body.model_dump()); store.resources.append(resource)
    bus.publish("resource.created",c["sub"],resource.model_dump()); return resource

@app.get("/admin/analytics/overview")
def analytics(c=Depends(current)):
    if c["role"] not in {"admin","institution_manager"}: raise HTTPException(403,"admin role required")
    return overview(store)
