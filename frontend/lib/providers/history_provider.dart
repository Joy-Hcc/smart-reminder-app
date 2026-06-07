import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/history.dart';
import '../services/api_service.dart';

final historyProvider = StateNotifierProvider<HistoryNotifier, AsyncValue<List<ReminderHistory>>>((ref) => HistoryNotifier());

class HistoryNotifier extends StateNotifier<AsyncValue<List<ReminderHistory>>> {
  HistoryNotifier() : super(const AsyncValue.data([]));

  Future<void> load({String? reminderId}) async {
    state = const AsyncValue.loading();
    try {
      final list = await ApiService().fetchHistory(reminderId: reminderId);
      state = AsyncValue.data(list);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }
}
