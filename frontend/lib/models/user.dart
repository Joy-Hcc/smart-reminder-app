class User {
  final String id;
  final String deviceId;
  final String? apiProvider;
  final DateTime createdAt;

  User({required this.id, required this.deviceId, this.apiProvider, required this.createdAt});

  factory User.fromJson(Map<String, dynamic> json) => User(
    id: json['id'],
    deviceId: json['device_id'],
    apiProvider: json['api_provider'],
    createdAt: DateTime.parse(json['created_at']),
  );
}
