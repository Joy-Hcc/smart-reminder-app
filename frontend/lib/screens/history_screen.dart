import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../services/api_service.dart';
import '../models/history.dart';

class HistoryScreen extends ConsumerStatefulWidget {
  const HistoryScreen({super.key});

  @override
  ConsumerState<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends ConsumerState<HistoryScreen> {
  Future<List<ReminderHistory>>? _future;

  @override
  void initState() {
    super.initState();
    _future = ApiService().fetchHistory();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('历史记录')),
      body: FutureBuilder(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snap.hasError) return Center(child: Text('错误: ${snap.error}'));
          final list = snap.data ?? [];
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
      ),
    );
  }
}
