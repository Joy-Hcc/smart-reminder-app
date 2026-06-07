import 'package:hive_flutter/hive_flutter.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class HiveStorage {
  HiveStorage._();
  static final HiveStorage instance = HiveStorage._();

  static const _boxName = 'app_settings';
  late final Box _box;
  late final FlutterSecureStorage _secureStorage;

  // Keys
  static const deviceIdKey = 'device_id';
  static const baseUrlKey = 'base_url';
  static const userKey = 'user_json';
  static const apiKeyKey = 'api_key';
  static const providerKey = 'api_provider';
  static const tokenKey = 'auth_token';

  static const defaultBaseUrl = 'http://10.241.224.231:8000';

  Future<void> init() async {
    await Hive.initFlutter();
    _box = await Hive.openBox(_boxName);
    _secureStorage = const FlutterSecureStorage();
    await Future.wait([_loadApiKey(), _loadToken()]);
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

  // API Key 使用安全存储
  String? _cachedApiKey;
  String? get apiKey => _cachedApiKey;
  Future<void> setApiKey(String key) async {
    _cachedApiKey = key;
    await _secureStorage.write(key: apiKeyKey, value: key);
  }
  Future<void> _loadApiKey() async {
    _cachedApiKey = await _secureStorage.read(key: apiKeyKey);
  }

  String? get apiProvider => getString(providerKey);
  Future<void> setApiProvider(String p) => setString(providerKey, p);

  // Token 也使用安全存储
  String? _cachedToken;
  String? get token => _cachedToken;
  Future<void> setToken(String t) async {
    _cachedToken = t;
    await _secureStorage.write(key: tokenKey, value: t);
  }
  Future<void> clearToken() async {
    _cachedToken = null;
    await _secureStorage.delete(key: tokenKey);
  }
  Future<void> _loadToken() async {
    _cachedToken = await _secureStorage.read(key: tokenKey);
  }
}
