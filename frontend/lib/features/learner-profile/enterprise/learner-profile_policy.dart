bool canProceedLearnerProfile(String action, {required bool reviewed, required bool ownerMatch}) {
  const protected = {'publish_content', 'institution_export', 'high_risk_intervention'};
  return ownerMatch && (!protected.contains(action) || reviewed);
}
