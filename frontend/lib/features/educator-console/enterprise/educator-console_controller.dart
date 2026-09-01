import 'educator-console_state.dart';

class EducatorConsoleController {
  EducatorConsoleState state = const EducatorConsoleState();
  void beginLoad() => state = const EducatorConsoleState(loading: true);
  void fail(String message) => state = EducatorConsoleState(error: message);
}
