class Category {
  final String id;
  final String name;
  final String? parentId;
  final String? icon;
  final int sortOrder;
  final List<Category> children;

  Category({required this.id, required this.name, this.parentId, this.icon, this.sortOrder = 0, this.children = const []});

  factory Category.fromJson(Map<String, dynamic> json) => Category(
    id: json['id'],
    name: json['name'],
    parentId: json['parent_id'],
    icon: json['icon'],
    sortOrder: json['sort_order'] ?? 0,
    children: (json['children'] as List<dynamic>? ?? []).map((e) => Category.fromJson(e)).toList(),
  );

  Map<String, dynamic> toJson() => {
    'name': name,
    'parent_id': parentId,
    'icon': icon,
    'sort_order': sortOrder,
  };
}
