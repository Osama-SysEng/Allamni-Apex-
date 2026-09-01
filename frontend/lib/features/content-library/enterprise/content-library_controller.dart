import 'content-library_state.dart';

class ContentLibraryController {
  ContentLibraryState state = const ContentLibraryState();
  void beginLoad() => state = const ContentLibraryState(loading: true);
  void fail(String message) => state = ContentLibraryState(error: message);
}
