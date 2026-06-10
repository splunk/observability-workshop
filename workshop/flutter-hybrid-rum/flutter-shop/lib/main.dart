import 'package:flutter/material.dart';

import 'src/app.dart';
import 'src/rum_config.dart';
import 'src/rum_service.dart';
import 'src/shop_api.dart';
import 'src/shop_store.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final config = RumConfig.fromEnvironment();
  await RumService.instance.install(config);

  final api = ShopApi(baseUrl: config.apiBaseUrl);
  final store = ShopStore(api: api);

  runApp(ShopApp(config: config, store: store));
}
