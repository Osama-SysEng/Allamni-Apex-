abstract interface class EducatorConsoleRepository {
  Future<List<Object>> load({String? cursor});
}
