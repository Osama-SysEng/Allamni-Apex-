def overview(store):
    students=len(store.profiles)
    completed=len([e for e in store.events if e.get("type")=="assessment.completed"])
    return {
        "students":students,
        "resources":len(store.resources),
        "learning_events":len(store.events),
        "assessment_completions":completed,
        "online_learning_ratio":0.0,
        "offline_learning_ratio":0.0,
        "course_performance":0.0,
        "student_progress":0.0,
        "engagement":0.0,
        "completion_rate":0.0
    }
