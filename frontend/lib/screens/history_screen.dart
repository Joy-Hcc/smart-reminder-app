import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../providers/history_provider.dart';

class HistoryScreen extends ConsumerStatefulWidget {
  const HistoryScreen({super.key});

  @override
  ConsumerState<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends ConsumerState<HistoryScreen> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() => ref.read(historyProvider.notifier).load());
  }

  @override
  Widget build(BuildContext context) {
    final historyAsync = ref.watch(historyProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('历史记录')),
      body: historyAsync.when(
        data: (list) {
          if (list.isEmpty) return const Center(child: Text('暂无记录'));
          return ListView.builder(
            itemCount: list.length,
            itemBuilder: (_, i) {
              final h = list[i];
              return ListTile(
                title: Text(h.triggerType ?? '提醒'),
                subtitle: Text(DateFormat('yyyy-MM-dd HH:mm').format(h.triggeredAt)),
                trailing: Icon(h.emailSent ? Icons.check_circle : Icons.error, color: h.emailSent ? Colors.green : Colors.red),
              );
            },
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(child: Text('错误: $e')),
      ),
    );
  }
}
