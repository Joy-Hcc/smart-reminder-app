import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../models/reminder.dart';
import '../providers/reminder_provider.dart';

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

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final dt = reminder.triggerType == 'scheduled'
        ? DateTime.tryParse(reminder.triggerConfig['datetime'] ?? '')
        : null;

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: _priorityColor(reminder.priority).withAlpha(40),
          child: Icon(Icons.alarm, color: _priorityColor(reminder.priority)),
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
            if (v == 'pause') await ref.read(reminderProvider.notifier).pause(reminder.id);
            if (v == 'resume') await ref.read(reminderProvider.notifier).resume(reminder.id);
            if (v == 'delete') await ref.read(reminderProvider.notifier).delete(reminder.id);
          },
          itemBuilder: (_) => [
            if (reminder.status == 'active')
              const PopupMenuItem(value: 'pause', child: Text('暂停')),
            if (reminder.status == 'paused')
              const PopupMenuItem(value: 'resume', child: Text('恢复')),
            const PopupMenuItem(value: 'delete', child: Text('删除')),
          ],
        ),
      ),
    );
  }
}
