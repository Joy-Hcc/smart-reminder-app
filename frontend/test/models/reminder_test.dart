import 'package:flutter_test/flutter_test.dart';
import 'package:smart_reminder/models/reminder.dart';

void main() {
  group('Reminder', () {
    test('fromJson parses all fields correctly', () {
      final json = {
        'id': 'rem-001',
        'category_id': 'cat-001',
        'title': 'Buy groceries',
        'description': 'Milk, eggs, bread',
        'priority': 'high',
        'trigger_type': 'scheduled',
        'trigger_config': {'datetime': '2026-06-01T10:00:00Z'},
        'advance_notice': 15,
        'repeat_rule': 'daily',
        'status': 'active',
        'created_at': '2026-05-23T08:00:00Z',
      };

      final reminder = Reminder.fromJson(json);

      expect(reminder.id, 'rem-001');
      expect(reminder.categoryId, 'cat-001');
      expect(reminder.title, 'Buy groceries');
      expect(reminder.description, 'Milk, eggs, bread');
      expect(reminder.priority, 'high');
      expect(reminder.triggerType, 'scheduled');
      expect(reminder.triggerConfig, {'datetime': '2026-06-01T10:00:00Z'});
      expect(reminder.advanceNotice, 15);
      expect(reminder.repeatRule, 'daily');
      expect(reminder.status, 'active');
      expect(reminder.createdAt, DateTime.parse('2026-05-23T08:00:00Z'));
    });

    test('fromJson handles null optional fields', () {
      final json = {
        'id': 'rem-002',
        'category_id': null,
        'title': 'Simple task',
        'description': null,
        'priority': 'medium',
        'trigger_type': 'event',
        'trigger_config': null,
        'advance_notice': null,
        'repeat_rule': null,
        'status': 'active',
        'created_at': '2026-05-23T08:00:00Z',
      };

      final reminder = Reminder.fromJson(json);

      expect(reminder.categoryId, isNull);
      expect(reminder.description, isNull);
      expect(reminder.triggerConfig, isEmpty);
      expect(reminder.advanceNotice, 0);
      expect(reminder.repeatRule, isNull);
    });

    test('toJson serializes correctly', () {
      final reminder = Reminder(
        id: 'rem-003',
        categoryId: 'cat-002',
        title: 'Meeting',
        description: 'Team standup',
        priority: 'low',
        triggerType: 'scheduled',
        triggerConfig: {'datetime': '2026-06-01T09:00:00Z'},
        advanceNotice: 5,
        repeatRule: 'weekly',
        status: 'active',
        createdAt: DateTime.parse('2026-05-23T08:00:00Z'),
      );

      final json = reminder.toJson();

      expect(json['category_id'], 'cat-002');
      expect(json['title'], 'Meeting');
      expect(json['description'], 'Team standup');
      expect(json['priority'], 'low');
      expect(json['trigger_type'], 'scheduled');
      expect(json['trigger_config'], {'datetime': '2026-06-01T09:00:00Z'});
      expect(json['advance_notice'], 5);
      expect(json['repeat_rule'], 'weekly');
      // toJson does not include id, status, created_at (server-generated)
      expect(json.containsKey('id'), isFalse);
      expect(json.containsKey('status'), isFalse);
      expect(json.containsKey('created_at'), isFalse);
    });

    test('default advanceNotice is 0', () {
      final reminder = Reminder(
        id: 'rem-004',
        title: 'No advance',
        priority: 'medium',
        triggerType: 'event',
        triggerConfig: {},
        status: 'active',
        createdAt: DateTime.parse('2026-05-23T08:00:00Z'),
      );

      expect(reminder.advanceNotice, 0);
    });

    test('fromJson with empty trigger_config defaults to empty map', () {
      final json = {
        'id': 'rem-005',
        'title': 'Empty config',
        'priority': 'medium',
        'trigger_type': 'event',
        'trigger_config': null,
        'status': 'active',
        'created_at': '2026-05-23T08:00:00Z',
      };

      final reminder = Reminder.fromJson(json);
      expect(reminder.triggerConfig, isEmpty);
    });

    test('fromJson with nested trigger_config', () {
      final json = {
        'id': 'rem-006',
        'title': 'Weather alert',
        'priority': 'high',
        'trigger_type': 'event',
        'trigger_config': {
          'event_type': 'weather',
          'event_config': {'condition': 'rain', 'city': 'Beijing'},
        },
        'status': 'active',
        'created_at': '2026-05-23T08:00:00Z',
      };

      final reminder = Reminder.fromJson(json);
      expect(reminder.triggerConfig['event_type'], 'weather');
      expect(reminder.triggerConfig['event_config']['city'], 'Beijing');
    });
  });
}
