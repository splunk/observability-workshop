import 'package:flutter/material.dart';

import '../app.dart';
import '../rum_service.dart';
import 'checkout_webview_screen.dart';

class CartScreen extends StatefulWidget {
  const CartScreen({super.key});

  static const routeName = '/cart';

  @override
  State<CartScreen> createState() => _CartScreenState();
}

class _CartScreenState extends State<CartScreen> {
  @override
  void initState() {
    super.initState();
    RumService.instance.trackScreen('CartScreen');
  }

  @override
  Widget build(BuildContext context) {
    final store = ShopScope.storeOf(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Cart')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (store.cart.isEmpty)
            const Text('Your cart is empty. Add a product before checkout.')
          else
            for (final item in store.cart)
              ListTile(
                title: Text(item.product.name),
                subtitle: Text('Quantity: ${item.quantity}'),
                trailing: Text('\$${item.total.toStringAsFixed(0)}'),
              ),
          const Divider(),
          ListTile(
            title: const Text('Total'),
            trailing: Text('\$${store.cartTotal.toStringAsFixed(0)}'),
          ),
          const SizedBox(height: 16),
          FilledButton.icon(
            icon: const Icon(Icons.lock_outline),
            label: const Text('Start checkout'),
            onPressed: store.cart.isEmpty
                ? null
                : () async {
                    await store.startCheckout();
                    if (!context.mounted) {
                      return;
                    }
                    await Navigator.of(context).push(
                      MaterialPageRoute<void>(
                        settings: const RouteSettings(
                          name: CheckoutWebViewScreen.routeName,
                        ),
                        builder: (_) => const CheckoutWebViewScreen(),
                      ),
                    );
                  },
          ),
        ],
      ),
    );
  }
}
