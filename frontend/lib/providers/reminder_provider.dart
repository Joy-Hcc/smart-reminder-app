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
    try {
      final created = await ApiService().createReminder(r);
      state = AsyncValue.data([created, ...state.value ?? []]);
    } catch (e) {
      rethrow;
    }
  }

  Future<void> update(String id, Reminder r) async {
    try {
      final updated = await ApiService().updateReminder(id, r);
      state = AsyncValue.data((state.value ?? []).map((x) => x.id == id ? updated : x).toList());
    } catch (e) {
      rethrow;
    }
  }

  Future<void> delete(String id) async {
    try {
      await ApiService().deleteReminder(id);
      state = AsyncValue.data((state.value ?? []).where((x) => x.id != id).toList());
    } catch (e) {
      rethrow;
    }
  }

  Future<void> pause(String id) async {
    try {
      await ApiService().pauseReminder(id);
      state = AsyncValue.data((state.value ?? []).map((x) => x.id == id ? Reminder(
        id: x.id, title: x.title, description: x.description, priority: x.priority,
        triggerType: x.triggerType, triggerConfig: x.triggerConfig, advanceNotice: x.advanceNotice,
        repeatRule: x.repeatRule, status: 'paused', createdAt: x.createdAt, categoryId: x.categoryId,
      ) : x).toList());
    } catch (e) {
      await load();
    }
  }

  Future<void> resume(String id) async {
    try {
      await ApiService().resumeReminder(id);
      state = AsyncValue.data((state.value ?? []).map((x) => x.id == id ? Reminder(
        id: x.id, title: x.title, description: x.description, priority: x.priority,
        triggerType: x.triggerType, triggerConfig: x.triggerConfig, advanceNotice: x.advanceNotice,
        repeatRule: x.repeatRule, status: 'active', createdAt: x.createdAt, categoryId: x.categoryId,
      ) : x).toList());
    } catch (e) {
      await load();
    }
  }
}
