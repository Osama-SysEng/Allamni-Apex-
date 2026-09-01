class ContentLibraryState {
  const ContentLibraryState({this.loading = false, this.error, this.items = const []});
  final bool loading;
  final String? error;
  final List<Object> items;
}
