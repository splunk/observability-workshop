class Product {
  const Product({
    required this.id,
    required this.name,
    required this.category,
    required this.description,
    required this.price,
    required this.tier,
  });

  final String id;
  final String name;
  final String category;
  final String description;
  final double price;
  final String tier;
}

class CartItem {
  const CartItem({
    required this.product,
    required this.quantity,
  });

  final Product product;
  final int quantity;

  double get total => product.price * quantity;

  CartItem incremented() {
    return CartItem(product: product, quantity: quantity + 1);
  }
}

class OrderResult {
  const OrderResult({
    required this.orderId,
    required this.total,
  });

  final String orderId;
  final double total;
}
