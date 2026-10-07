import 'tutor-session_state.dart';

class TutorSessionController {
  TutorSessionState state = const TutorSessionState();
  void beginLoad() => state = const TutorSessionState(loading: true);
  void fail(String message) => state = TutorSessionState(error: message);
}
