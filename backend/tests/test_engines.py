from shared.models import LearningProfile, Skill, LearningPreferences, Resource
from shared.engines import build_roadmap, recommend_next_action, update_mastery

def make_profile():
    return LearningProfile(student_id="1",goal_domain="software",
      learning_preferences=LearningPreferences(content_format=["interactive"]),
      skills=[Skill(code="oop",name="OOP",level=.2,target=.8,confidence=.4,importance=1)])

def test_mastery_increases():
    level,confidence=update_mastery(.2,.4,.9)
    assert level>.2 and confidence>.4

def test_roadmap():
    result=build_roadmap(make_profile())
    assert result["nodes"][0]["skill_code"]=="oop"

def test_recommendation():
    r=Resource(id="r",title="OOP",platform="x",url="https://example.com",
      skills=["oop"],attributes=["interactive"],duration_minutes=90,quality_score=.9)
    result=recommend_next_action(make_profile(),[r])
    assert result.resource.id=="r"


def test_cognitive_risk_and_agent_loop():
    from shared.intelligence import cognitive_snapshot, risk_score, AgentOrchestrator
    p=make_profile()
    snap=cognitive_snapshot(p)
    assert 0 <= snap["mastery"] <= 1
    assert risk_score(p)["level"] in {"low","medium","high","critical"}
    trace=AgentOrchestrator().run(p)
    assert trace["trace_id"] and len(trace["decisions"]) == 4

def test_adaptive_difficulty_moves_with_performance():
    from shared.intelligence import adaptive_difficulty
    assert adaptive_difficulty(.5,.95,.8) > .5
    assert adaptive_difficulty(.5,.2,.3) < .5

def test_event_bus_is_idempotent():
    from shared.events import EventBus
    from shared.store import MemoryStore
    s=MemoryStore(); b=EventBus(s)
    a=b.publish("x","student",{"v":1}); c=b.publish("x","student",{"v":1})
    assert a["id"] == c["id"] and len(s.events)==1

def test_content_blueprint_has_adaptive_sequence():
    from shared.content import lesson_blueprint
    from shared.store import MemoryStore
    p=make_profile(); s=MemoryStore(); s.seed()
    bp=lesson_blueprint(p,s.resources)
    assert bp["sequence"][-1]["type"] == "micro_assessment"
    assert "mind_map" in [x["type"] for x in bp["sequence"]]

def test_token_roundtrip_and_tamper_detection():
    from shared.security import create_token, decode_token
    token=create_token("student-1","student")
    assert decode_token(token)["sub"] == "student-1"
    parts=token.split('.')
    parts[1]=parts[1][:-1] + ('A' if parts[1][-1] != 'A' else 'B')
    try: decode_token('.'.join(parts))
    except ValueError: pass
    else: assert False, "tampered token accepted"
