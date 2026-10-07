abstract interface class LearnerProfileRepository {
  Future<List<Object>> load({String? cursor});
}
