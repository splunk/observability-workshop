import 'dart:convert';
import 'dart:math';

import 'package:http/http.dart' as http;

import 'models.dart';

class ShopApi {
  ShopApi({
    required String baseUrl,
    http.Client? client,
  })  : _baseUrl = baseUrl.endsWith('/')
            ? baseUrl.substring(0, baseUrl.length - 1)
            : baseUrl,
        _client = client ?? http.Client();

  final String _baseUrl;
  final http.Client _client;

  static const products = <Product>[
    Product(
      id: 'baseline-monitor',
      name: 'Baseline Monitor',
      category: 'observability',
      description: 'Fast startup, stable rendering, and clean network timing.',
      price: 49,
      tier: 'standard',
    ),
    Product(
      id: 'replay-analyzer',
      name: 'Replay Analyzer',
      category: 'digital-experience',
      description: 'Correlates replay, user actions, and front-end errors.',
      price: 129,
      tier: 'premium',
    ),
    Product(
      id: 'checkout-tracer',
      name: 'Checkout Tracer',
      category: 'apm',
      description: 'Links slow mobile checkout steps to backend traces.',
      price: 199,
      tier: 'premium',
    ),
  ];

  Future<List<Product>> fetchProducts() async {
    await _get('/anything/products');
    return products;
  }

  Future<void> addToCart(Product product) async {
    await _post('/anything/cart', {
      'product_id': product.id,
      'quantity': 1,
    });
  }

  Future<OrderResult> submitOrder({
    required List<CartItem> items,
    required double total,
  }) async {
    await _post('/anything/checkout', {
      'item_count': items.fold<int>(0, (sum, item) => sum + item.quantity),
      'total': total,
    });

    final id = Random().nextInt(900000) + 100000;
    return OrderResult(orderId: 'ORD-$id', total: total);
  }

  Uri _uri(String path) => Uri.parse('$_baseUrl$path');

  Future<void> _get(String path) async {
    try {
      await _client.get(_uri(path)).timeout(const Duration(seconds: 5));
    } catch (_) {
      // The sample still works when the network is unavailable. The request is
      // only present so RUM has real mobile network activity when possible.
    }
  }

  Future<void> _post(String path, Map<String, Object?> payload) async {
    try {
      await _client
          .post(
            _uri(path),
            headers: {'content-type': 'application/json'},
            body: jsonEncode(payload),
          )
          .timeout(const Duration(seconds: 5));
    } catch (_) {
      // Keep the workshop app usable offline or behind a restrictive proxy.
    }
  }
}
