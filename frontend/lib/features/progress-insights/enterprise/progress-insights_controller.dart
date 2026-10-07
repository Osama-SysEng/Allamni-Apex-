import 'progress-insights_state.dart';

class ProgressInsightsController {
  ProgressInsightsState state = const ProgressInsightsState();
  void beginLoad() => state = const ProgressInsightsState(loading: true);
  void fail(String message) => state = ProgressInsightsState(error: message);
}
