import 'package:flutter/material.dart';
import '../models/category.dart';

class CategoryTree extends StatelessWidget {
  final List<Category> categories;
  final ValueChanged<Category>? onTap;
  const CategoryTree({super.key, required this.categories, this.onTap});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: categories.length,
      itemBuilder: (_, i) => _buildNode(categories[i]),
    );
  }

  Widget _buildNode(Category cat, {int depth = 0}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        ListTile(
          contentPadding: EdgeInsets.only(left: 16.0 + depth * 24),
          leading: cat.icon != null ? Icon(IconData(int.parse(cat.icon!), fontFamily: 'MaterialIcons')) : const Icon(Icons.folder),
          title: Text(cat.name),
          onTap: onTap != null ? () => onTap!(cat) : null,
        ),
        ...cat.children.map((c) => _buildNode(c, depth: depth + 1)),
      ],
    );
  }
}
