REVIEW_ACTIONS = {"PUBLISH_CONTENT", "INSTITUTION_EXPORT", "HIGH_RISK_INTERVENTION", "EXTERNAL_MEDIA"}

def requires_human_review(action: str, learner_age_band: str = "adult") -> bool:
    return action.upper() in REVIEW_ACTIONS or learner_age_band.lower() in {"child", "minor"}

def may_expose_personalisation(owner_match: bool, consent: bool) -> bool:
    return owner_match and consent
