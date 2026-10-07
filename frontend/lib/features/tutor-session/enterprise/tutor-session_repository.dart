abstract interface class TutorSessionRepository {
  Future<List<Object>> load({String? cursor});
}
