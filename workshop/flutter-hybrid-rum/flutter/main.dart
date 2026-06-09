import 'package:flutter/widgets.dart';
import 'package:splunk_otel_flutter/splunk_otel_flutter.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await SplunkRum.instance.install(
    agentConfiguration: AgentConfiguration(
      endpoint: EndpointConfiguration.forRum(
        realm: const String.fromEnvironment('SPLUNK_RUM_REALM'),
        rumAccessToken: const String.fromEnvironment('SPLUNK_RUM_ACCESS_TOKEN'),
      ),
      appName: const String.fromEnvironment(
        'SPLUNK_RUM_APPLICATION_NAME',
        defaultValue: 'mobile-checkout',
      ),
      deploymentEnvironment: const String.fromEnvironment(
        'SPLUNK_RUM_ENVIRONMENT',
        defaultValue: 'workshop',
      ),
      appVersion: const String.fromEnvironment(
        'SPLUNK_RUM_APP_VERSION',
        defaultValue: '0.0.0-dev',
      ),
    ),
    moduleConfigurations: [
      NavigationModuleConfiguration(isEnabled: true),
      InteractionsModuleConfiguration(isEnabled: true),
      CrashReportsModuleConfiguration(isEnabled: true),
    ],
  );

  await configureRumContext(buildFlavor: 'debug', tenantTier: 'workshop');

  runApp(const MyApp());
}

Future<void> configureRumContext({
  required String buildFlavor,
  required String tenantTier,
}) async {
  await SplunkRum.instance.user.preferences.setTrackingMode(
    trackingMode: UserTrackingMode.anonymousTracking,
  );

  await SplunkRum.instance.globalAttributes.setAll(
    attributes: MutableAttributes(
      attributes: {
        'app.platform': MutableAttributeString(value: 'flutter'),
        'app.build_flavor': MutableAttributeString(value: buildFlavor),
        'tenant.tier': MutableAttributeString(value: tenantTier),
      },
    ),
  );
}

Future<void> trackCheckoutExample(Future<void> Function() submitOrder) async {
  final workflow = await SplunkRum.instance.customTracking.startWorkflow(
    name: 'checkout',
  );

  try {
    await submitOrder();
    await workflow.end();
  } catch (error) {
    await SplunkRum.instance.customTracking.trackCustomEvent(
      name: 'checkout_failed',
      attributes: MutableAttributes(
        attributes: {
          'error.type': MutableAttributeString(
            value: error.runtimeType.toString(),
          ),
        },
      ),
    );
    await workflow.end();
    rethrow;
  }
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const Directionality(
      textDirection: TextDirection.ltr,
      child: Text('Replace this placeholder with your app root.'),
    );
  }
}
