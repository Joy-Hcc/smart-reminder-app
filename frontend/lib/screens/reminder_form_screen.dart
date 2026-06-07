import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../models/reminder.dart';
import '../providers/reminder_provider.dart';
import '../providers/category_provider.dart';

class ReminderFormScreen extends ConsumerStatefulWidget {
  final Reminder? reminder;
  const ReminderFormScreen({super.key, this.reminder});

  @override
  ConsumerState<ReminderFormScreen> createState() => _ReminderFormScreenState();
}

class _ReminderFormScreenState extends ConsumerState<ReminderFormScreen> {
  final _titleCtrl = TextEditingController();
  final _descCtrl = TextEditingController();
  String _priority = 'medium';
  String _triggerType = 'scheduled';
  DateTime? _scheduledTime;
  String? _categoryId;
  String _repeatRule = '';

  bool get _isEdit => widget.reminder != null;

  @override
  void initState() {
    super.initState();
    Future.microtask(() => ref.read(categoryProvider.notifier).load());
    if (_isEdit) {
      final r = widget.reminder!;
      _titleCtrl.text = r.title;
      _descCtrl.text = r.description ?? '';
      _priority = r.priority;
      _triggerType = r.triggerType;
      _categoryId = r.categoryId;
      _repeatRule = r.repeatRule ?? '';
      if (r.triggerType == 'scheduled' && r.triggerConfig['datetime'] != null) {
        _scheduledTime = DateTime.tryParse(r.triggerConfig['datetime']);
      }
    }
  }

  Future<void> _pickDateTime() async {
    final d = await showDatePicker(
      context: context,
      initialDate: _scheduledTime ?? DateTime.now().add(const Duration(minutes: 5)),
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365)),
    );
    if (d == null || !mounted) return;
    final t = await showTimePicker(
      context: context,
      initialTime: _scheduledTime != null
          ? TimeOfDay.fromDateTime(_scheduledTime!)
          : TimeOfDay.now(),
    );
    if (t == null || !mounted) return;
    setState(() => _scheduledTime = DateTime(d.year, d.month, d.day, t.hour, t.minute));
  }

  Future<void> _submit() async {
    if (_titleCtrl.text.isEmpty || (_triggerType == 'scheduled' && _scheduledTime == null)) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('请填写完整信息')));
      return;
    }
    final r = Reminder(
      id: _isEdit ? widget.reminder!.id : '',
      title: _titleCtrl.text,
      description: _descCtrl.text.isEmpty ? null : _descCtrl.text,
      priority: _priority,
      triggerType: _triggerType,
      triggerConfig: _triggerType == 'scheduled'
          ? {'datetime': _scheduledTime!.toIso8601String()}
          : {'event_type': 'weather'},
      categoryId: _categoryId,
      repeatRule: _repeatRule.isEmpty ? null : _repeatRule,
      status: _isEdit ? widget.reminder!.status : 'active',
      createdAt: _isEdit ? widget.reminder!.createdAt : DateTime.now(),
    );

    try {
      final notifier = ref.read(reminderProvider.notifier);
      if (_isEdit) {
        await notifier.update(widget.reminder!.id, r);
      } else {
        await notifier.add(r);
      }
      if (mounted) Navigator.pop(context);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('保存失败: $e')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final catsAsync = ref.watch(categoryProvider);

    return Scaffold(
      appBar: AppBar(title: Text(_isEdit ? '编辑提醒' : '新建提醒')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(controller: _titleCtrl, decoration: const InputDecoration(labelText: '标题', border: OutlineInputBorder())),
            const SizedBox(height: 12),
            TextField(controller: _descCtrl, decoration: const InputDecoration(labelText: '描述', border: OutlineInputBorder()), maxLines: 3),
            const SizedBox(height: 12),
            catsAsync.when(
              data: (cats) => DropdownButtonFormField<String>(
                value: _categoryId,
                hint: const Text('选择分类'),
                items: [
                  const DropdownMenuItem(value: null, child: Text('无分类')),
                  ...cats.expand((c) => [c, ...c.children]).map((c) => DropdownMenuItem(value: c.id, child: Text(c.name))),
                ],
                onChanged: (v) => setState(() => _categoryId = v),
                decoration: const InputDecoration(border: OutlineInputBorder()),
              ),
              loading: () => const LinearProgressIndicator(),
              error: (_, __) => const SizedBox(),
            ),
            const SizedBox(height: 12),
            SegmentedButton<String>(
              segments: const [
                ButtonSegment(value: 'high', label: Text('高')),
                ButtonSegment(value: 'medium', label: Text('中')),
                ButtonSegment(value: 'low', label: Text('低')),
              ],
              selected: {_priority},
              onSelectionChanged: (s) => setState(() => _priority = s.first),
            ),
            const SizedBox(height: 12),
            SegmentedButton<String>(
              segments: const [
                ButtonSegment(value: 'scheduled', label: Text('定时')),
                ButtonSegment(value: 'event', label: Text('事件')),
              ],
              selected: {_triggerType},
              onSelectionChanged: (s) => setState(() => _triggerType = s.first),
            ),
            const SizedBox(height: 12),
            if (_triggerType == 'scheduled')
              ListTile(
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                tileColor: Theme.of(context).colorScheme.surfaceContainerHighest,
                title: Text(_scheduledTime == null ? '选择时间' : DateFormat('yyyy-MM-dd HH:mm').format(_scheduledTime!)),
                trailing: const Icon(Icons.calendar_today),
                onTap: _pickDateTime,
              ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: FilledButton(onPressed: _submit, child: Text(_isEdit ? '更新' : '保存')),
            ),
          ],
        ),
      ),
    );
  }
}
