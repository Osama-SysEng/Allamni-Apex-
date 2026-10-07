import 'learning-roadmap_state.dart';

class LearningRoadmapController {
  LearningRoadmapState state = const LearningRoadmapState();
  void beginLoad() => state = const LearningRoadmapState(loading: true);
  void fail(String message) => state = LearningRoadmapState(error: message);
}
