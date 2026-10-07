import 'diagnostic-assessment_state.dart';

class DiagnosticAssessmentController {
  DiagnosticAssessmentState state = const DiagnosticAssessmentState();
  void beginLoad() => state = const DiagnosticAssessmentState(loading: true);
  void fail(String message) => state = DiagnosticAssessmentState(error: message);
}
