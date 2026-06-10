import 'package:flutter/material.dart';

import '../app.dart';
import '../rum_service.dart';

class InstrumentationExamplesScreen extends StatefulWidget {
  const InstrumentationExamplesScreen({super.key});

  static const routeName = '/instrumentation-examples';

  @override
  State<InstrumentationExamplesScreen> createState() =>
      _InstrumentationExamplesScreenState();
}

class _InstrumentationExamplesScreenState
    extends State<InstrumentationExamplesScreen> {
  String _status = 'Choose an example to generate telemetry.';

  @override
  void initState() {
    super.initState();
    RumService.instance.trackScreen('InstrumentationExamplesScreen');
  }

  @override
  Widget build(BuildContext context) {
    final store = ShopScope.storeOf(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Instrumentation examples')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(
            'Automatic instrumentation',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 8),
          const Text(
            'These examples rely on the agent modules enabled during startup. '
            'The button below does not call Splunk RUM directly. It makes a '
            'normal HTTP request through app code, which should be captured by '
            'network instrumentation when live RUM is enabled.',
          ),
          const SizedBox(height: 12),
          FilledButton.icon(
            icon: const Icon(Icons.cloud_sync_outlined),
            label: const Text('Generate automatic network request'),
            onPressed: () async {
              setState(() => _status = 'Calling demo backend...');
              await store.runAutoNetworkExample();
              setState(() {
                _status =
                    'Network example complete. Check RUM network requests.';
              });
            },
          ),
          const SizedBox(height: 24),
          Text(
            'Custom instrumentation',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 8),
          const Text(
            'These examples call the Splunk RUM custom tracking API directly '
            'because the business meaning cannot be inferred automatically.',
          ),
          const SizedBox(height: 12),
          OutlinedButton.icon(
            icon: const Icon(Icons.label_outline),
            label: const Text('Send custom event'),
            onPressed: () async {
              await RumService.instance.trackWorkshopMilestone(
                scenario: 'manual_button_press',
              );
              setState(() {
                _status = 'Custom event sent: workshop_custom_event.';
              });
            },
          ),
          const SizedBox(height: 8),
          OutlinedButton.icon(
            icon: const Icon(Icons.timer_outlined),
            label: const Text('Run custom workflow'),
            onPressed: () async {
              setState(() => _status = 'Running custom workflow...');
              await RumService.instance.runTrainingWorkflow();
              setState(() {
                _status =
                    'Custom workflow ended: manual_instrumentation_training.';
              });
            },
          ),
          const SizedBox(height: 24),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Text(_status),
            ),
          ),
        ],
      ),
    );
  }
}
