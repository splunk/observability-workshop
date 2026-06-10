import 'package:flutter/material.dart';

import 'rum_config.dart';
import 'rum_service.dart';
import 'screens/catalog_screen.dart';
import 'screens/telemetry_screen.dart';
import 'shop_store.dart';

class ShopApp extends StatelessWidget {
  const ShopApp({
    required this.config,
    required this.store,
    super.key,
  });

  final RumConfig config;
  final ShopStore store;

  @override
  Widget build(BuildContext context) {
    return ShopScope(
      config: config,
      store: store,
      child: MaterialApp(
        title: 'Flutter Hybrid RUM Shop',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xffbd0d5f)),
          useMaterial3: true,
        ),
        home: const CatalogScreen(),
        routes: {
          TelemetryScreen.routeName: (_) => const TelemetryScreen(),
        },
        navigatorObservers: [RumNavigationObserver()],
      ),
    );
  }
}

class ShopScope extends InheritedNotifier<ShopStore> {
  const ShopScope({
    required this.config,
    required ShopStore store,
    required super.child,
    super.key,
  }) : super(notifier: store);

  final RumConfig config;

  static ShopStore storeOf(BuildContext context) {
    final scope = context.dependOnInheritedWidgetOfExactType<ShopScope>();
    assert(scope != null, 'ShopScope was not found in the widget tree.');
    return scope!.notifier!;
  }

  static RumConfig configOf(BuildContext context) {
    final scope = context.dependOnInheritedWidgetOfExactType<ShopScope>();
    assert(scope != null, 'ShopScope was not found in the widget tree.');
    return scope!.config;
  }
}

class RumNavigationObserver extends NavigatorObserver {
  @override
  void didPush(Route<dynamic> route, Route<dynamic>? previousRoute) {
    super.didPush(route, previousRoute);
    final name = route.settings.name;
    if (name != null && name.isNotEmpty) {
      RumService.instance.trackScreen(name);
    }
  }
}
