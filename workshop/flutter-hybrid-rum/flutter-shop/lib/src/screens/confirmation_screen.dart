import 'package:flutter/material.dart';

import '../models.dart';
import '../rum_service.dart';

class ConfirmationScreen extends StatefulWidget {
  const ConfirmationScreen({required this.order, super.key});

  static const routeName = '/confirmation';

  final OrderResult order;

  @override
  State<ConfirmationScreen> createState() => _ConfirmationScreenState();
}

class _ConfirmationScreenState extends State<ConfirmationScreen> {
  @override
  void initState() {
    super.initState();
    RumService.instance.trackScreen('ConfirmationScreen');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Order confirmed')),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                Icons.check_circle_outline,
                size: 96,
                color: Theme.of(context).colorScheme.primary,
              ),
              const SizedBox(height: 16),
              Text(
                'Order ${widget.order.orderId}',
                style: Theme.of(context).textTheme.headlineSmall,
              ),
              const SizedBox(height: 8),
              Text('Total: \$${widget.order.total.toStringAsFixed(0)}'),
              const SizedBox(height: 24),
              FilledButton(
                onPressed: () => Navigator.of(context).popUntil(
                  (route) => route.isFirst,
                ),
                child: const Text('Back to catalog'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
