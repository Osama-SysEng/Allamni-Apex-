from shared.models import RoadmapNode, Recommendation, Resource, LearningProfile

def update_mastery(level, confidence, performance, weight=1):
    level=max(0,min(1,level)); confidence=max(0,min(1,confidence)); performance=max(0,min(1,performance))
    alpha=max(.05,min(1,weight*(.35+.65*confidence)))
    return round((1-alpha)*level+alpha*performance,4), round(min(1,confidence+weight*.08),4)

def build_roadmap(profile:LearningProfile):
    gaps=[]
    for s in profile.skills:
        gap=max(0,s.target-s.level)
        if gap>.05: gaps.append((gap*s.importance,s))
    gaps.sort(key=lambda x:x[0],reverse=True)
    nodes=[]
    for i,(priority,s) in enumerate(gaps,1):
        nodes.append(RoadmapNode(id=f"node_{i}",skill_code=s.code,title=f"تطوير {s.name}",
            sequence=i,priority=round(priority,4),mastery_current=s.level,mastery_target=s.target))
    return {"student_id":profile.student_id,"status":"generated","nodes":[n.model_dump() for n in nodes]}

def recommend_next_action(profile, resources:list[Resource]):
    gaps=[s for s in profile.skills if s.target>s.level]
    if not gaps:
        return Recommendation(action_type="celebrate",message="أتممت أهدافك الحالية. انتقل إلى مهارة متقدمة.")
    target=max(gaps,key=lambda s:(s.target-s.level)*s.importance)
    preferred=set(profile.learning_preferences.content_format)
    best=None; best_score=-1
    for r in resources:
        score=0
        if target.code in r.skills: score+=.55
        score+=r.quality_score*.20
        if preferred.intersection(r.attributes): score+=.15
        if r.duration_minutes and r.duration_minutes<=180: score+=.10
        if score>best_score: best,best_score=r,score
    if not best:
        return Recommendation(action_type="add_resources",message="لا توجد مصادر تعليمية كافية.")
    reasons=[f"يعالج الفجوة في {target.name}"]
    if preferred.intersection(best.attributes): reasons.append("يتوافق مع تفضيلات تعلمك")
    return Recommendation(action_type="start_resource",message="هذه أفضل خطوة تعليمية تالية لك.",
        skill_code=target.code,resource=best,score=round(best_score,4),reasons=reasons)

def score_assessment(responses):
    if not responses:return {"score":0,"correct":0,"total":0}
    scores=[float(r.get("score",1 if r.get("correct") else 0)) for r in responses]
    return {"score":round(sum(scores)/len(scores),4),"correct":sum(1 for x in scores if x>=.5),"total":len(scores)}
