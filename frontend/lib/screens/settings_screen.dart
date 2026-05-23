import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/auth_provider.dart';

class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  final _apiKeyCtrl = TextEditingController();
  String _provider = 'DeepSeek';
  final _providers = ['DeepSeek', 'OpenAI', 'Claude', '通义千问', '文心一言'];

  @override
  Widget build(BuildContext context) {
    final auth = ref.watch(authProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('设置')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('API 设置', style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: _provider,
              items: _providers.map((p) => DropdownMenuItem(value: p, child: Text(p))).toList(),
              onChanged: (v) => setState(() => _provider = v!),
              decoration: const InputDecoration(labelText: 'AI 厂商', border: OutlineInputBorder()),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _apiKeyCtrl,
              decoration: const InputDecoration(labelText: 'API KEY', border: OutlineInputBorder()),
              obscureText: true,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: auth.isLoading ? null : () {
                  ref.read(authProvider.notifier).verify(
                    apiKey: _apiKeyCtrl.text.trim(),
                    provider: _provider,
                  );
                },
                child: auth.isLoading ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2)) : const Text('保存并验证'),
              ),
            ),
            if (auth.value != null)
              Padding(
                padding: const EdgeInsets.only(top: 16),
                child: Text('已绑定设备: ${auth.value!.deviceId.substring(0, 8)}...', style: const TextStyle(color: Colors.green)),
              ),
          ],
        ),
      ),
    );
  }
}
