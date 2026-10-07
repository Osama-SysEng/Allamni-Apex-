abstract interface class ProgressInsightsRepository {
  Future<List<Object>> load({String? cursor});
}
