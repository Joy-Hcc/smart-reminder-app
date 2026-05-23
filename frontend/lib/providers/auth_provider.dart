import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/user.dart';
import '../services/api_service.dart';

final authProvider = StateNotifierProvider<AuthNotifier, AsyncValue<User?>>((ref) => AuthNotifier());

class AuthNotifier extends StateNotifier<AsyncValue<User?>> {
  AuthNotifier() : super(const AsyncValue.data(null)) {
    _restoreFromCache();
  }

  /// Restore user from Hive on startup (offline support).
  void _restoreFromCache() {
    final cached = ApiService().getCachedUser();
    if (cached != null) {
      state = AsyncValue.data(cached);
    }
  }

  Future<void> verify({String? apiKey, String? provider}) async {
    state = const AsyncValue.loading();
    try {
      final user = await ApiService().verifyAuth(apiKey: apiKey, provider: provider);
      state = AsyncValue.data(user);
    } catch (e, st) {
      // On network failure, fall back to cached user if available
      final cached = ApiService().getCachedUser();
      if (cached != null) {
        state = AsyncValue.data(cached);
      } else {
        state = AsyncValue.error(e, st);
      }
    }
  }

  /// Clear cached user (logout).
  Future<void> logout() async {
    state = const AsyncValue.data(null);
    await ApiService().updateBaseUrl(''); // reset to default if needed
  }
}
