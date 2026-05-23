import 'dart:convert';
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:device_info_plus/device_info_plus.dart';
import '../models/user.dart';
import '../models/category.dart';
import '../models/reminder.dart';
import '../models/history.dart';
import 'hive_storage.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  final _storage = HiveStorage.instance;

  late final Dio _dio = Dio(BaseOptions(
    baseUrl: _storage.baseUrl,
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
    headers: {'Content-Type': 'application/json'},
  ));

  String? _deviceId;

  /// Get device ID, with Hive cache to avoid repeated device_info calls.
  Future<String> getDeviceId() async {
    if (_deviceId != null) return _deviceId!;

    // Try Hive cache first
    final cached = _storage.deviceId;
    if (cached.isNotEmpty) {
      _deviceId = cached;
      return _deviceId!;
    }

    // First time: query platform
    final plugin = DeviceInfoPlugin();
    if (Platform.isAndroid) {
      _deviceId = (await plugin.androidInfo).id;
    } else if (Platform.isIOS) {
      _deviceId = (await plugin.iosInfo).identifierForVendor;
    } else {
      _deviceId = 'unknown-platform';
    }

    // Persist to Hive
    await _storage.setDeviceId(_deviceId!);
    return _deviceId!;
  }

  /// Change the API base URL at runtime and persist to Hive.
  void updateBaseUrl(String newUrl) {
    _dio.options.baseUrl = newUrl;
    _storage.setBaseUrl(newUrl);
  }

  void setDeviceHeader() async {
    final id = await getDeviceId();
    _dio.options.headers['x-device-id'] = id;
  }

  /// Verify authentication and cache user info for offline use.
  Future<User> verifyAuth({String? apiKey, String? provider}) async {
    final id = await getDeviceId();
    final res = await _dio.post('/api/auth/verify', data: {
      'device_id': id,
      'api_key': apiKey,
      'api_provider': provider,
    });
    await setDeviceHeader();
    final user = User.fromJson(res.data);

    // Persist user + credentials for offline mode
    await _storage.setUserJson(jsonEncode(res.data));
    if (apiKey != null) await _storage.setApiKey(apiKey);
    if (provider != null) await _storage.setApiProvider(provider);

    return user;
  }

  /// Restore cached user from Hive (for offline / cold start).
  User? getCachedUser() {
    final json = _storage.userJson;
    if (json == null) return null;
    try {
      return User.fromJson(jsonDecode(json));
    } catch (_) {
      return null;
    }
  }

  String? get cachedApiKey => _storage.apiKey;
  String? get cachedProvider => _storage.apiProvider;

  Future<List<Category>> fetchCategories() async {
    await setDeviceHeader();
    final res = await _dio.get('/api/categories');
    return (res.data as List).map((e) => Category.fromJson(e)).toList();
  }

  Future<Category> createCategory(Category cat) async {
    await setDeviceHeader();
    final res = await _dio.post('/api/categories', data: cat.toJson());
    return Category.fromJson(res.data);
  }

  Future<List<Reminder>> fetchReminders({String? categoryId, String? status, String? search, int page = 1, int pageSize = 20}) async {
    await setDeviceHeader();
    final res = await _dio.get('/api/reminders', queryParameters: {
      if (categoryId != null) 'category_id': categoryId,
      if (status != null) 'status': status,
      if (search != null) 'search': search,
      'page': page,
      'page_size': pageSize,
    });
    return (res.data['items'] as List).map((e) => Reminder.fromJson(e)).toList();
  }

  Future<Reminder> createReminder(Reminder reminder) async {
    await setDeviceHeader();
    final res = await _dio.post('/api/reminders', data: reminder.toJson());
    return Reminder.fromJson(res.data);
  }

  Future<Reminder> updateReminder(String id, Reminder reminder) async {
    await setDeviceHeader();
    final res = await _dio.put('/api/reminders/$id', data: reminder.toJson());
    return Reminder.fromJson(res.data);
  }

  Future<void> deleteReminder(String id) async {
    await setDeviceHeader();
    await _dio.delete('/api/reminders/$id');
  }

  Future<void> pauseReminder(String id) async {
    await setDeviceHeader();
    await _dio.post('/api/reminders/$id/pause');
  }

  Future<void> resumeReminder(String id) async {
    await setDeviceHeader();
    await _dio.post('/api/reminders/$id/resume');
  }

  Future<List<ReminderHistory>> fetchHistory({String? reminderId, int page = 1, int pageSize = 50}) async {
    await setDeviceHeader();
    final res = await _dio.get('/api/history', queryParameters: {
      if (reminderId != null) 'reminder_id': reminderId,
      'page': page,
      'page_size': pageSize,
    });
    return (res.data['items'] as List).map((e) => ReminderHistory.fromJson(e)).toList();
  }
}
