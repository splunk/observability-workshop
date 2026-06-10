import 'package:flutter/material.dart';

import '../app.dart';
import '../models.dart';
import '../rum_service.dart';

class ProductDetailScreen extends StatefulWidget {
  const ProductDetailScreen({required this.product, super.key});

  final Product product;

  @override
  State<ProductDetailScreen> createState() => _ProductDetailScreenState();
}

class _ProductDetailScreenState extends State<ProductDetailScreen> {
  @override
  void initState() {
    super.initState();
    RumService.instance.trackScreen('ProductDetailScreen');
    RumService.instance.trackProductViewed(widget.product);
  }

  @override
  Widget build(BuildContext context) {
    final store = ShopScope.storeOf(context);

    return Scaffold(
      appBar: AppBar(title: Text(widget.product.name)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Icon(
            Icons.inventory_2_outlined,
            size: 96,
            color: Theme.of(context).colorScheme.primary,
          ),
          const SizedBox(height: 16),
          Text(
            widget.product.name,
            style: Theme.of(context).textTheme.headlineMedium,
          ),
          const SizedBox(height: 8),
          Text(widget.product.description),
          const SizedBox(height: 12),
          Text('Category: ${widget.product.category}'),
          Text('Tier: ${widget.product.tier}'),
          Text('Price: \$${widget.product.price.toStringAsFixed(0)}'),
          const SizedBox(height: 24),
          FilledButton.icon(
            icon: const Icon(Icons.add_shopping_cart),
            label: const Text('Add to cart'),
            onPressed: () => store.addToCart(widget.product),
          ),
        ],
      ),
    );
  }
}
