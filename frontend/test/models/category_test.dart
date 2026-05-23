import 'package:flutter_test/flutter_test.dart';
import 'package:smart_reminder/models/category.dart';

void main() {
  group('Category', () {
    test('fromJson parses all fields correctly', () {
      final json = {
        'id': 'cat-001',
        'name': 'Work',
        'parent_id': null,
        'icon': 'briefcase',
        'sort_order': 2,
        'children': [],
        'created_at': '2026-05-23T08:00:00Z',
      };

      final category = Category.fromJson(json);

      expect(category.id, 'cat-001');
      expect(category.name, 'Work');
      expect(category.parentId, isNull);
      expect(category.icon, 'briefcase');
      expect(category.sortOrder, 2);
      expect(category.children, isEmpty);
    });

    test('fromJson with nested children', () {
      final json = {
        'id': 'cat-001',
        'name': 'Personal',
        'parent_id': null,
        'icon': null,
        'sort_order': 0,
        'children': [
          {
            'id': 'cat-002',
            'name': 'Health',
            'parent_id': 'cat-001',
            'icon': 'heart',
            'sort_order': 0,
            'children': [
              {
                'id': 'cat-003',
                'name': 'Exercise',
                'parent_id': 'cat-002',
                'icon': null,
                'sort_order': 0,
                'children': [],
              }
            ],
          },
          {
            'id': 'cat-004',
            'name': 'Finance',
            'parent_id': 'cat-001',
            'icon': 'money',
            'sort_order': 1,
            'children': [],
          },
        ],
      };

      final category = Category.fromJson(json);

      expect(category.name, 'Personal');
      expect(category.children.length, 2);

      final health = category.children[0];
      expect(health.name, 'Health');
      expect(health.parentId, 'cat-001');
      expect(health.icon, 'heart');
      expect(health.children.length, 1);
      expect(health.children[0].name, 'Exercise');

      final finance = category.children[1];
      expect(finance.name, 'Finance');
      expect(finance.icon, 'money');
    });

    test('fromJson with null children defaults to empty list', () {
      final json = {
        'id': 'cat-005',
        'name': 'Empty',
        'sort_order': 0,
        'children': null,
      };

      final category = Category.fromJson(json);
      expect(category.children, isEmpty);
    });

    test('fromJson defaults sort_order to 0 when missing', () {
      final json = {
        'id': 'cat-006',
        'name': 'No Order',
        'children': [],
      };

      final category = Category.fromJson(json);
      expect(category.sortOrder, 0);
    });

    test('toJson serializes correctly', () {
      final category = Category(
        id: 'cat-007',
        name: 'Meeting',
        parentId: 'cat-001',
        icon: 'calendar',
        sortOrder: 3,
      );

      final json = category.toJson();

      expect(json['name'], 'Meeting');
      expect(json['parent_id'], 'cat-001');
      expect(json['icon'], 'calendar');
      expect(json['sort_order'], 3);
      // toJson does not include id or children (server-generated)
      expect(json.containsKey('id'), isFalse);
      expect(json.containsKey('children'), isFalse);
    });

    test('toJson with null parentId', () {
      final category = Category(
        id: 'cat-008',
        name: 'Root',
        sortOrder: 0,
      );

      final json = category.toJson();
      expect(json['parent_id'], isNull);
      expect(json['icon'], isNull);
    });

    test('category constructor defaults', () {
      final category = Category(id: 'x', name: 'Test');

      expect(category.parentId, isNull);
      expect(category.icon, isNull);
      expect(category.sortOrder, 0);
      expect(category.children, isEmpty);
    });
  });
}
