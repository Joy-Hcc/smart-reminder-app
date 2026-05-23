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
  @override
  void initState() {
    super.initState();
    Future.microtask(() => ref.read(reminderProvider.notifier).load());
  }

  @override
  Widget build(BuildContext context) {
    final remindersAsync = ref.watch(reminderProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('智能提醒'),
        actions: [
          IconButton(icon: const Icon(Icons.history), onPressed: () => Navigator.pushNamed(context, AppRoutes.history)),
          IconButton(icon: const Icon(Icons.settings), onPressed: () => Navigator.pushNamed(context, AppRoutes.settings)),
        ],
      ),
      body: remindersAsync.when(
        data: (list) {
          if (list.isEmpty) {
            return const Center(child: Text('暂无提醒，点击右下角添加'));
          }
          return ListView.builder(
            itemCount: list.length,
            itemBuilder: (_, i) => ReminderCard(reminder: list[i]),
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(child: Text('加载失败: $e')),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => Navigator.pushNamed(context, AppRoutes.reminderForm),
        child: const Icon(Icons.add),
      ),
    );
  }
}
