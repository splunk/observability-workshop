import 'package:flutter/foundation.dart';

import 'models.dart';
import 'rum_service.dart';
import 'shop_api.dart';

class ShopStore extends ChangeNotifier {
  ShopStore({required ShopApi api}) : _api = api;

  final ShopApi _api;

  bool isLoading = false;
  List<Product> products = const [];
  final List<CartItem> cart = [];
  OrderResult? lastOrder;

  int get itemCount => cart.fold<int>(0, (sum, item) => sum + item.quantity);

  double get cartTotal {
    return cart.fold<double>(0, (sum, item) => sum + item.total);
  }

  Future<void> loadProducts() async {
    if (products.isNotEmpty || isLoading) {
      return;
    }

    isLoading = true;
    notifyListeners();

    products = await _api.fetchProducts();

    isLoading = false;
    notifyListeners();
  }

  Future<void> runAutoNetworkExample() async {
    await _api.fetchProducts();
  }

  Future<void> addToCart(Product product) async {
    await _api.addToCart(product);

    final index = cart.indexWhere((item) => item.product.id == product.id);
    if (index == -1) {
      cart.add(CartItem(product: product, quantity: 1));
    } else {
      cart[index] = cart[index].incremented();
    }

    await RumService.instance.trackCartItemAdded(product, itemCount);
    notifyListeners();
  }

  Future<void> startCheckout() async {
    await RumService.instance.startCheckout(cartTotal);
  }

  Future<OrderResult> submitOrder() async {
    try {
      final result = await _api.submitOrder(items: cart, total: cartTotal);
      lastOrder = result;
      cart.clear();
      await RumService.instance.completeCheckout(result);
      notifyListeners();
      return result;
    } catch (error) {
      await RumService.instance.failCheckout(error);
      rethrow;
    }
  }
}
