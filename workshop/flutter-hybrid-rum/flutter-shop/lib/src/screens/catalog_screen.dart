import 'package:flutter/material.dart';

import '../app.dart';
import '../models.dart';
import '../rum_service.dart';
import 'cart_screen.dart';
import 'product_detail_screen.dart';
import 'telemetry_screen.dart';

class CatalogScreen extends StatefulWidget {
  const CatalogScreen({super.key});

  static const routeName = '/catalog';

  @override
  State<CatalogScreen> createState() => _CatalogScreenState();
}

class _CatalogScreenState extends State<CatalogScreen> {
  @override
  void initState() {
    super.initState();
    RumService.instance.trackScreen('CatalogScreen');
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ShopScope.storeOf(context).loadProducts();
    });
  }

  @override
  Widget build(BuildContext context) {
    final store = ShopScope.storeOf(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Flutter Hybrid RUM Shop'),
        actions: [
          IconButton(
            tooltip: 'Telemetry status',
            icon: const Icon(Icons.sensors),
            onPressed: () => Navigator.of(context).pushNamed(
              TelemetryScreen.routeName,
            ),
          ),
          IconButton(
            tooltip: 'Cart',
            icon: Badge(
              label: Text('${store.itemCount}'),
              child: const Icon(Icons.shopping_cart_outlined),
            ),
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute<void>(
                settings: const RouteSettings(name: CartScreen.routeName),
                builder: (_) => const CartScreen(),
              ),
            ),
          ),
        ],
      ),
      body: store.isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                Text(
                  'Instrumented mobile checkout',
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
                const SizedBox(height: 8),
                const Text(
                  'Browse products, add one to cart, then open the embedded '
                  'WebView checkout to generate Flutter RUM and browser RUM.',
                ),
                const SizedBox(height: 16),
                for (final product in store.products)
                  _ProductTile(product: product),
              ],
            ),
    );
  }
}

class _ProductTile extends StatelessWidget {
  const _ProductTile({required this.product});

  final Product product;

  @override
  Widget build(BuildContext context) {
    final store = ShopScope.storeOf(context);

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(product.name, style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 4),
            Text(product.description),
            const SizedBox(height: 8),
            Text('\$${product.price.toStringAsFixed(0)}'),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              children: [
                OutlinedButton.icon(
                  icon: const Icon(Icons.visibility_outlined),
                  label: const Text('View'),
                  onPressed: () => Navigator.of(context).push(
                    MaterialPageRoute<void>(
                      settings: RouteSettings(
                        name: '/product/${product.id}',
                      ),
                      builder: (_) => ProductDetailScreen(product: product),
                    ),
                  ),
                ),
                FilledButton.icon(
                  icon: const Icon(Icons.add_shopping_cart),
                  label: const Text('Add to cart'),
                  onPressed: () => store.addToCart(product),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
