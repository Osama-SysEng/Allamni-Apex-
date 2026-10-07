abstract interface class LearningRoadmapRepository {
  Future<List<Object>> load({String? cursor});
}
