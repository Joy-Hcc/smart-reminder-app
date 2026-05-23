class ReminderHistory {
  final String id;
  final String reminderId;
  final DateTime triggeredAt;
  final String? triggerType;
  final String? content;
  final bool emailSent;

  ReminderHistory({
    required this.id,
    required this.reminderId,
    required this.triggeredAt,
    this.triggerType,
    this.content,
    required this.emailSent,
  });

  factory ReminderHistory.fromJson(Map<String, dynamic> json) => ReminderHistory(
    id: json['id'],
    reminderId: json['reminder_id'],
    triggeredAt: DateTime.parse(json['triggered_at']),
    triggerType: json['trigger_type'],
    content: json['content'],
    emailSent: json['email_sent'] ?? false,
  );
}
