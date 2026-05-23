import 'package:hive_flutter/hive_flutter.dart';

class HiveStorage {
  HiveStorage._();
  static final HiveStorage instance = HiveStorage._();

  static const _boxName = 'app_settings';
  late final Box _box;

  // Keys
  static const deviceIdKey = 'device_id';
  static const baseUrlKey = 'base_url';
  static const userKey = 'user_json';
  static const apiKeyKey = 'api_key';
  static const providerKey = 'api_provider';

  static const defaultBaseUrl = 'http://10.241.224.231:8000';

  Future<void> init() async {
    await Hive.initFlutter();
    _box = await Hive.openBox(_boxName);
  }

  // -- Generic helpers --
  String? getString(String key) => _box.get(key) as String?;
  Future<void> setString(String key, String value) => _box.put(key, value);

  // -- Typed accessors --
  String get deviceId => getString(deviceIdKey) ?? '';
  Future<void> setDeviceId(String id) => setString(deviceIdKey, id);

  String get baseUrl => getString(baseUrlKey) ?? defaultBaseUrl;
  Future<void> setBaseUrl(String url) => setString(baseUrlKey, url);

  String? get userJson => getString(userKey);
  Future<void> setUserJson(String json) => setString(userKey, json);

  String? get apiKey => getString(apiKeyKey);
  Future<void> setApiKey(String key) => setString(apiKeyKey, key);

  String? get apiProvider => getString(providerKey);
  Future<void> setApiProvider(String p) => setString(providerKey, p);
}
