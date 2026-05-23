class Reminder {
  final String id;
  final String? categoryId;
  final String title;
  final String? description;
  final String priority;
  final String triggerType;
  final Map<String, dynamic> triggerConfig;
  final int advanceNotice;
  final String? repeatRule;
  final String status;
  final DateTime createdAt;

  Reminder({
    required this.id,
    this.categoryId,
    required this.title,
    this.description,
    required this.priority,
    required this.triggerType,
    required this.triggerConfig,
    this.advanceNotice = 0,
    this.repeatRule,
    required this.status,
    required this.createdAt,
  });

  factory Reminder.fromJson(Map<String, dynamic> json) => Reminder(
    id: json['id'],
    categoryId: json['category_id'],
    title: json['title'],
    description: json['description'],
    priority: json['priority'],
    triggerType: json['trigger_type'],
    triggerConfig: Map<String, dynamic>.from(json['trigger_config'] ?? {}),
    advanceNotice: json['advance_notice'] ?? 0,
    repeatRule: json['repeat_rule'],
    status: json['status'],
    createdAt: DateTime.parse(json['created_at']),
  );

  Map<String, dynamic> toJson() => {
    'category_id': categoryId,
    'title': title,
    'description': description,
    'priority': priority,
    'trigger_type': triggerType,
    'trigger_config': triggerConfig,
    'advance_notice': advanceNotice,
    'repeat_rule': repeatRule,
  };
}
