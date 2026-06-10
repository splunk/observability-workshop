import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:webview_flutter/webview_flutter.dart';

import '../app.dart';
import '../rum_service.dart';
import 'confirmation_screen.dart';

class CheckoutWebViewScreen extends StatefulWidget {
  const CheckoutWebViewScreen({super.key});

  static const routeName = '/checkout-webview';

  @override
  State<CheckoutWebViewScreen> createState() => _CheckoutWebViewScreenState();
}

class _CheckoutWebViewScreenState extends State<CheckoutWebViewScreen> {
  late final WebViewController _controller;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    RumService.instance.trackScreen('CheckoutWebViewScreen');
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageFinished: (_) => setState(() => _loading = false),
        ),
      )
      ..addJavaScriptChannel(
        'CheckoutBridge',
        onMessageReceived: _handleCheckoutMessage,
      );

    WidgetsBinding.instance.addPostFrameCallback((_) => _loadCheckout());
  }

  Future<void> _loadCheckout() async {
    final config = ShopScope.configOf(context);
    final store = ShopScope.storeOf(context);
    final html = await rootBundle.loadString('assets/web/checkout.html');
    final rumConfig = jsonEncode({
      'enabled': config.liveRumEnabled,
      'realm': config.realm,
      'rumAccessToken': config.accessToken,
      'applicationName': config.hybridApplicationName,
      'environment': config.environment,
      'appVersion': config.appVersion,
      'apiBaseUrl': config.apiBaseUrl,
      'agentVersion': config.rumAgentVersion,
      'shell': 'flutter',
      'cartTotal': store.cartTotal,
    });

    await _controller.loadHtmlString(
      html.replaceFirst('__RUM_CONFIG_JSON__', rumConfig),
    );
  }

  Future<void> _handleCheckoutMessage(JavaScriptMessage message) async {
    final store = ShopScope.storeOf(context);
    if (message.message == 'complete') {
      final order = await store.submitOrder();
      if (!mounted) {
        return;
      }
      await Navigator.of(context).pushReplacement(
        MaterialPageRoute<void>(
          settings: const RouteSettings(name: ConfirmationScreen.routeName),
          builder: (_) => ConfirmationScreen(order: order),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('WebView checkout')),
      body: Stack(
        children: [
          WebViewWidget(controller: _controller),
          if (_loading) const Center(child: CircularProgressIndicator()),
        ],
      ),
    );
  }
}
