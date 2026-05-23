import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/reminder.dart';
import '../services/api_service.dart';

final reminderProvider = StateNotifierProvider<ReminderNotifier, AsyncValue<List<Reminder>>>((ref) => ReminderNotifier());

class ReminderNotifier extends StateNotifier<AsyncValue<List<Reminder>>> {
  ReminderNotifier() : super(const AsyncValue.data([]));

  Future<void> load({String? categoryId, String? status, String? search}) async {
    state = const AsyncValue.loading();
    try {
      final list = await ApiService().fetchReminders(categoryId: categoryId, status: status, search: search);
      state = AsyncValue.data(list);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> add(Reminder r) async {
    final created = await ApiService().createReminder(r);
    state = AsyncValue.data([created, ...state.value ?? []]);
  }

  Future<void> update(String id, Reminder r) async {
    final updated = await ApiService().updateReminder(id, r);
    state = AsyncValue.data((state.value ?? []).map((x) => x.id == id ? updated : x).toList());
  }

  Future<void> delete(String id) async {
    await ApiService().deleteReminder(id);
    state = AsyncValue.data((state.value ?? []).where((x) => x.id != id).toList());
  }

  Future<void> pause(String id) async {
    await ApiService().pauseReminder(id);
    await load();
  }

  Future<void> resume(String id) async {
    await ApiService().resumeReminder(id);
    await load();
  }
}
