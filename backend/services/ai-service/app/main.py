from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from shared.security import decode_token
from shared.store import store
from shared.intelligence import AgentOrchestrator, cognitive_snapshot, risk_score
from shared.content import lesson_blueprint
from .providers import get_provider

app=FastAPI(title="Allamni AI Service", version="3.0.0")
orchestrator=AgentOrchestrator(); provider=get_provider()

class AnalyzeRequest(BaseModel): student_id:str
class GenerateRequest(BaseModel): student_id:str; prompt:str="Create adaptive learning material"; context:dict={}

def auth(authorization):
    if not authorization.startswith("Bearer "): raise HTTPException(401,"missing token")
    try:return decode_token(authorization[7:])
    except Exception as e:raise HTTPException(401,str(e))

@app.get("/health")
def health():return {"status":"ok","service":"ai","version":"3.0.0"}

@app.post("/students/analyze")
def analyze(body:AnalyzeRequest,authorization:str=Header("")):
    c=auth(authorization)
    if c["sub"]!=body.student_id and c["role"] not in {"admin","institution_manager"}: raise HTTPException(403,"forbidden")
    profile=store.profiles.get(body.student_id)
    if not profile:raise HTTPException(404,"profile not found")
    return {"cognitive":cognitive_snapshot(profile),"risk":risk_score(profile),"orchestration":orchestrator.run(profile),"provider":provider.__class__.__name__}

@app.post("/students/generate-plan")
def generate_plan(body:AnalyzeRequest,authorization:str=Header("")):
    c=auth(authorization)
    if c["sub"]!=body.student_id and c["role"] not in {"admin","institution_manager"}: raise HTTPException(403,"forbidden")
    profile=store.profiles.get(body.student_id)
    if not profile:raise HTTPException(404,"profile not found")
    return {"plan":lesson_blueprint(profile,store.resources),"analysis":provider.analyze(profile.model_dump()),"provider":provider.__class__.__name__}

@app.post("/students/generate")
def generate(body:GenerateRequest,authorization:str=Header("")):
    c=auth(authorization)
    if c["sub"]!=body.student_id and c["role"] not in {"admin","institution_manager"}: raise HTTPException(403,"forbidden")
    profile=store.profiles.get(body.student_id)
    if not profile: raise HTTPException(404,"profile not found")
    return provider.generate(body.prompt,body.context | {"profile":profile.model_dump()})
