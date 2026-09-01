abstract interface class DiagnosticAssessmentRepository {
  Future<List<Object>> load({String? cursor});
}
