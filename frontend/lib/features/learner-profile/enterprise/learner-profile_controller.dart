import 'learner-profile_state.dart';

class LearnerProfileController {
  LearnerProfileState state = const LearnerProfileState();
  void beginLoad() => state = const LearnerProfileState(loading: true);
  void fail(String message) => state = LearnerProfileState(error: message);
}
