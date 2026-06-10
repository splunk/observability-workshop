import 'package:flutter/material.dart';

import '../app.dart';
import '../rum_service.dart';
import 'instrumentation_examples_screen.dart';

class TelemetryScreen extends StatefulWidget {
  const TelemetryScreen({super.key});

  static const routeName = '/telemetry';

  @override
  State<TelemetryScreen> createState() => _TelemetryScreenState();
}

class _TelemetryScreenState extends State<TelemetryScreen> {
  @override
  void initState() {
    super.initState();
    RumService.instance.trackScreen('TelemetryScreen');
  }

  @override
  Widget build(BuildContext context) {
    final config = ShopScope.configOf(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Telemetry status')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _StatusTile(
            label: 'Live Flutter RUM',
            value: RumService.instance.enabled ? 'enabled' : 'disabled',
          ),
          _StatusTile(label: 'RUM app', value: config.applicationName),
          _StatusTile(label: 'WebView RUM app', value: config.hybridApplicationName),
          _StatusTile(label: 'Environment', value: config.environment),
          _StatusTile(label: 'App version', value: config.appVersion),
          _StatusTile(label: 'Backend target', value: config.apiBaseUrl),
          const SizedBox(height: 16),
          const Text(
            'Instrumentation points',
            style: TextStyle(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          const Text(
            '1. Flutter RUM installs before runApp().\n'
            '2. Product and cart actions create custom events.\n'
            '3. Checkout is wrapped in a custom workflow.\n'
            '4. The WebView page initializes browser RUM.\n'
            '5. API calls create network telemetry for RUM/APM validation.',
          ),
          const SizedBox(height: 24),
          FilledButton.icon(
            icon: const Icon(Icons.play_circle_outline),
            label: const Text('Open instrumentation examples'),
            onPressed: () => Navigator.of(context).pushNamed(
              InstrumentationExamplesScreen.routeName,
            ),
          ),
        ],
      ),
    );
  }
}

class _StatusTile extends StatelessWidget {
  const _StatusTile({required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return ListTile(
      contentPadding: EdgeInsets.zero,
      title: Text(label),
      subtitle: Text(value),
    );
  }
}
