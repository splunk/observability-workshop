import 'package:flutter/foundation.dart';
import 'package:splunk_otel_flutter/splunk_otel_flutter.dart';

import 'models.dart';
import 'rum_config.dart';

class RumService {
  RumService._();

  static final RumService instance = RumService._();

  bool _enabled = false;
  dynamic _checkoutWorkflow;

  bool get enabled => _enabled;

  // Automatic instrumentation is enabled during install. The app does not call
  // Splunk RUM for every tap, route change, lifecycle transition, crash, slow
  // render, or supported network request. The enabled modules observe those
  // signals after the agent is installed.
  Future<void> install(RumConfig config) async {
    if (!config.liveRumEnabled) {
      debugPrint('Splunk RUM disabled: using placeholder RUM token.');
      return;
    }

    try {
      await SplunkRum.instance.install(
        agentConfiguration: AgentConfiguration(
          endpoint: EndpointConfiguration.forRum(
            realm: config.realm,
            rumAccessToken: config.accessToken,
          ),
          appName: config.applicationName,
          deploymentEnvironment: config.environment,
          appVersion: config.appVersion,
        ),
        moduleConfigurations: [
          NavigationModuleConfiguration(isEnabled: true),
          InteractionsModuleConfiguration(isEnabled: true),
          CrashReportsModuleConfiguration(isEnabled: true),
          SlowRenderingModuleConfiguration(
            isEnabled: true,
            interval: const Duration(seconds: 1),
          ),
          AnrModuleConfiguration(isEnabled: true),
        ],
      );

      await SplunkRum.instance.user.preferences.setTrackingMode(
        trackingMode: UserTrackingMode.anonymousTracking,
      );

      await SplunkRum.instance.globalAttributes.setAll(
        attributes: MutableAttributes(
          attributes: {
            'app.version': MutableAttributeString(value: config.appVersion),
            'app.platform': MutableAttributeString(value: 'flutter'),
            'app.shell': MutableAttributeString(value: 'flutter'),
            'app.build_flavor': MutableAttributeString(value: 'workshop'),
            'tenant.tier': MutableAttributeString(value: 'demo'),
          },
        ),
      );

      _enabled = true;
      debugPrint('Splunk RUM initialized for ${config.applicationName}.');
    } catch (error, stackTrace) {
      debugPrint('Splunk RUM initialization failed: $error');
      debugPrint('$stackTrace');
    }
  }

  Future<void> trackScreen(String screenName) async {
    if (!_enabled) {
      return;
    }
    await _safeCall(
      () => SplunkRum.instance.navigation.track(screenName: screenName),
    );
  }

  // Custom instrumentation starts here. These methods add app-specific meaning
  // that automatic instrumentation cannot infer from framework activity alone.
  Future<void> trackProductViewed(Product product) async {
    if (!_enabled) {
      return;
    }
    await _safeCall(
      () => SplunkRum.instance.customTracking.trackCustomEvent(
        name: 'product_viewed',
        attributes: MutableAttributes(
          attributes: {
            'product.id': MutableAttributeString(value: product.id),
            'product.category': MutableAttributeString(value: product.category),
            'product.price': MutableAttributeDouble(value: product.price),
          },
        ),
      ),
    );
  }

  Future<void> trackCartItemAdded(Product product, int quantity) async {
    if (!_enabled) {
      return;
    }
    await _safeCall(
      () => SplunkRum.instance.customTracking.trackCustomEvent(
        name: 'cart_item_added',
        attributes: MutableAttributes(
          attributes: {
            'product.id': MutableAttributeString(value: product.id),
            'product.category': MutableAttributeString(value: product.category),
            'cart.item_quantity': MutableAttributeInt(value: quantity),
          },
        ),
      ),
    );
  }

  Future<void> trackWorkshopMilestone({required String scenario}) async {
    if (!_enabled) {
      return;
    }
    await _safeCall(
      () => SplunkRum.instance.customTracking.trackCustomEvent(
        name: 'workshop_custom_event',
        attributes: MutableAttributes(
          attributes: {
            'workshop.scenario': MutableAttributeString(value: scenario),
            'instrumentation.type': MutableAttributeString(value: 'custom'),
          },
        ),
      ),
    );
  }

  Future<void> runTrainingWorkflow() async {
    if (!_enabled) {
      return;
    }
    await _safeCall(() async {
      final workflow = await SplunkRum.instance.customTracking.startWorkflow(
        name: 'manual_instrumentation_training',
      );
      await Future<void>.delayed(const Duration(milliseconds: 400));
      await SplunkRum.instance.customTracking.trackCustomEvent(
        name: 'manual_instrumentation_training_step',
        attributes: MutableAttributes(
          attributes: {
            'workshop.step': MutableAttributeString(value: 'examples_screen'),
            'instrumentation.type': MutableAttributeString(value: 'custom'),
          },
        ),
      );
      await Future<void>.delayed(const Duration(milliseconds: 250));
      await workflow.end();
    });
  }

  Future<void> startCheckout(double cartTotal) async {
    if (!_enabled) {
      return;
    }
    await _safeCall(() async {
      _checkoutWorkflow = await SplunkRum.instance.customTracking.startWorkflow(
        name: 'checkout',
      );
      await SplunkRum.instance.customTracking.trackCustomEvent(
        name: 'checkout_started',
        attributes: MutableAttributes(
          attributes: {
            'cart.total': MutableAttributeDouble(value: cartTotal),
          },
        ),
      );
    });
  }

  Future<void> completeCheckout(OrderResult result) async {
    if (!_enabled) {
      return;
    }
    await _safeCall(() async {
      await SplunkRum.instance.customTracking.trackCustomEvent(
        name: 'checkout_completed',
        attributes: MutableAttributes(
          attributes: {
            'order.total': MutableAttributeDouble(value: result.total),
          },
        ),
      );
      await _checkoutWorkflow?.end();
      _checkoutWorkflow = null;
    });
  }

  Future<void> failCheckout(Object error) async {
    if (!_enabled) {
      return;
    }
    await _safeCall(() async {
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
      await _checkoutWorkflow?.end();
      _checkoutWorkflow = null;
    });
  }

  Future<void> _safeCall(Future<void> Function() call) async {
    try {
      await call();
    } catch (error, stackTrace) {
      debugPrint('RUM call failed: $error');
      debugPrint('$stackTrace');
    }
  }
}
