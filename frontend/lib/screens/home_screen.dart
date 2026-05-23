import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../config/routes.dart';
import '../providers/reminder_provider.dart';
import '../widgets/reminder_card.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  String _searchQuery = '';
  bool _showSearch = false;

  @override
  void initState() {
    super.initState();
    Future.microtask(() => ref.read(reminderProvider.notifier).load());
  }

  void _onSearch(String query) {
    setState(() => _searchQuery = query);
    ref.read(reminderProvider.notifier).load(search: query.isEmpty ? null : query);
  }

  Future<void> _onRefresh() async {
    await ref.read(reminderProvider.notifier).load(
      search: _searchQuery.isEmpty ? null : _searchQuery,
    );
  }

  @override
  Widget build(BuildContext context) {
    final remindersAsync = ref.watch(reminderProvider);

    return Scaffold(
      appBar: AppBar(
        title: _showSearch
            ? TextField(
                autofocus: true,
                decoration: const InputDecoration(hintText: '搜索提醒...', border: InputBorder.none),
                onChanged: _onSearch,
              )
            : const Text('智能提醒'),
        actions: [
          IconButton(
            icon: Icon(_showSearch ? Icons.close : Icons.search),
            onPressed: () {
              setState(() {
                _showSearch = !_showSearch;
                if (!_showSearch) {
                  _searchQuery = '';
                  ref.read(reminderProvider.notifier).load();
                }
              });
            },
          ),
          IconButton(icon: const Icon(Icons.history), onPressed: () => Navigator.pushNamed(context, AppRoutes.history)),
          IconButton(icon: const Icon(Icons.settings), onPressed: () => Navigator.pushNamed(context, AppRoutes.settings)),
        ],
      ),
      body: remindersAsync.when(
        data: (list) {
          if (list.isEmpty) {
            return Center(child: Text(_searchQuery.isEmpty ? '暂无提醒，点击右下角添加' : '没有找到匹配的提醒'));
          }
          return RefreshIndicator(
            onRefresh: _onRefresh,
            child: ListView.builder(
              physics: const AlwaysScrollableScrollPhysics(),
              itemCount: list.length,
              itemBuilder: (_, i) => ReminderCard(reminder: list[i]),
            ),
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('加载失败: $e'),
              const SizedBox(height: 12),
              FilledButton(onPressed: _onRefresh, child: const Text('重试')),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => Navigator.pushNamed(context, AppRoutes.reminderForm),
        child: const Icon(Icons.add),
      ),
    );
  }
}
