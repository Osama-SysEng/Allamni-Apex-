abstract interface class ContentLibraryRepository {
  Future<List<Object>> load({String? cursor});
}
