import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../models/reminder.dart';
import '../providers/reminder_provider.dart';
import '../screens/reminder_form_screen.dart';

class ReminderCard extends ConsumerWidget {
  final Reminder reminder;
  const ReminderCard({super.key, required this.reminder});

  Color _priorityColor(String p) {
    return switch (p) {
      'high' => Colors.red,
      'medium' => Colors.orange,
      _ => Colors.green,
    };
  }

  Future<bool> _confirmDelete(BuildContext context) async {
    return await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('确认删除'),
        content: Text('确定要删除「${reminder.title}」吗？'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('取消')),
          TextButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('删除', style: TextStyle(color: Colors.red))),
        ],
      ),
    ) ?? false;
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final pc = _priorityColor(reminder.priority);
    final dt = reminder.triggerType == 'scheduled'
        ? DateTime.tryParse(reminder.triggerConfig['datetime'] ?? '')
        : null;

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: pc.withAlpha(60),
          child: Icon(Icons.alarm, color: pc),
        ),
        title: Text(reminder.title, maxLines: 1, overflow: TextOverflow.ellipsis),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (reminder.description != null)
              Text(reminder.description!, maxLines: 1, overflow: TextOverflow.ellipsis, style: Theme.of(context).textTheme.bodySmall),
            if (dt != null)
              Text(DateFormat('MM-dd HH:mm').format(dt), style: Theme.of(context).textTheme.bodySmall),
          ],
        ),
        trailing: PopupMenuButton<String>(
          onSelected: (v) async {
            try {
              if (v == 'edit') {
                Navigator.push(context, MaterialPageRoute(
                  builder: (_) => ReminderFormScreen(reminder: reminder),
                ));
              }
              if (v == 'pause') await ref.read(reminderProvider.notifier).pause(reminder.id);
              if (v == 'resume') await ref.read(reminderProvider.notifier).resume(reminder.id);
              if (v == 'delete' && await _confirmDelete(context)) {
                await ref.read(reminderProvider.notifier).delete(reminder.id);
              }
            } catch (e) {
              if (context.mounted) {
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('操作失败: $e')));
              }
            }
          },
          itemBuilder: (_) => [
            const PopupMenuItem(value: 'edit', child: Text('编辑')),
            if (reminder.status == 'active')
              const PopupMenuItem(value: 'pause', child: Text('暂停')),
            if (reminder.status == 'paused')
              const PopupMenuItem(value: 'resume', child: Text('恢复')),
            const PopupMenuItem(value: 'delete', child: Text('删除', style: TextStyle(color: Colors.red))),
          ],
        ),
      ),
    );
  }
}
