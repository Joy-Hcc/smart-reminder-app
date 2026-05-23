import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/auth_provider.dart';
import '../services/api_service.dart';
import '../services/hive_storage.dart';

class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  final _apiKeyCtrl = TextEditingController();
  final _serverUrlCtrl = TextEditingController();
  String _provider = 'DeepSeek';
  final _providers = ['DeepSeek', 'OpenAI', 'Claude', '通义千问', '文心一言'];
  bool _serverSaved = false;

  @override
  void initState() {
    super.initState();
    _serverUrlCtrl.text = HiveStorage.instance.baseUrl;
  }

  void _saveServerUrl() {
    final url = _serverUrlCtrl.text.trim();
    if (url.isEmpty) return;
    ApiService().updateBaseUrl(url);
    setState(() => _serverSaved = true);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('服务器地址已保存: $url')),
    );
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) setState(() => _serverSaved = false);
    });
  }

  @override
  Widget build(BuildContext context) {
    final auth = ref.watch(authProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('设置')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('服务器设置', style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 12),
            TextField(
              controller: _serverUrlCtrl,
              decoration: const InputDecoration(
                labelText: '服务器地址',
                hintText: 'http://192.168.x.x:8000',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 8),
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: _saveServerUrl,
                icon: Icon(_serverSaved ? Icons.check : Icons.save),
                label: Text(_serverSaved ? '已保存' : '保存服务器地址'),
              ),
            ),
            const Divider(height: 32),
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
