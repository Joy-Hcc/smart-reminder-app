import 'package:dio/dio.dart';
import 'package:device_info_plus/device_info_plus.dart';
import '../models/user.dart';
import '../models/category.dart';
import '../models/reminder.dart';
import '../models/history.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  final Dio _dio = Dio(BaseOptions(
    baseUrl: 'http://10.0.2.2:8000', // Android emulator localhost
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
    headers: {'Content-Type': 'application/json'},
  ));

  String? _deviceId;

  Future<String> getDeviceId() async {
    if (_deviceId != null) return _deviceId!;
    final info = await DeviceInfoPlugin().androidInfo;
    _deviceId = info.id;
    return _deviceId!;
  }

  void setDeviceHeader() async {
    final id = await getDeviceId();
    _dio.options.headers['x-device-id'] = id;
  }

  Future<User> verifyAuth({String? apiKey, String? provider}) async {
    final id = await getDeviceId();
    final res = await _dio.post('/api/auth/verify', data: {
      'device_id': id,
      'api_key': apiKey,
      'api_provider': provider,
    });
    await setDeviceHeader();
    return User.fromJson(res.data);
  }

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

  Future<List<Reminder>> fetchReminders({String? categoryId, String? status, String? search}) async {
    await setDeviceHeader();
    final res = await _dio.get('/api/reminders', queryParameters: {
      if (categoryId != null) 'category_id': categoryId,
      if (status != null) 'status': status,
      if (search != null) 'search': search,
    });
    return (res.data as List).map((e) => Reminder.fromJson(e)).toList();
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

  Future<List<ReminderHistory>> fetchHistory({String? reminderId, int limit = 50}) async {
    await setDeviceHeader();
    final res = await _dio.get('/api/history', queryParameters: {
      if (reminderId != null) 'reminder_id': reminderId,
      'limit': limit,
    });
    return (res.data as List).map((e) => ReminderHistory.fromJson(e)).toList();
  }
}
