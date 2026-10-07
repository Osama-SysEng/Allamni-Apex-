class EducatorConsoleState {
  const EducatorConsoleState({this.loading = false, this.error, this.items = const []});
  final bool loading;
  final String? error;
  final List<Object> items;
}
