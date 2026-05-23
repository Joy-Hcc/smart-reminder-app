import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/category.dart';
import '../services/api_service.dart';

final categoryProvider = StateNotifierProvider<CategoryNotifier, AsyncValue<List<Category>>>((ref) => CategoryNotifier());

class CategoryNotifier extends StateNotifier<AsyncValue<List<Category>>> {
  CategoryNotifier() : super(const AsyncValue.data([]));

  Future<void> load() async {
    state = const AsyncValue.loading();
    try {
      final list = await ApiService().fetchCategories();
      state = AsyncValue.data(list);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> add(Category cat) async {
    try {
      final created = await ApiService().createCategory(cat);
      state = AsyncValue.data([...state.value ?? [], created]);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }
}
