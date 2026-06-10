---
title: 2. Configure Flutter RUM
weight: 2
---

The Flutter path instruments the mobile shell: app launch, lifecycle, Flutter navigation, interactions, supported crash signals, and HTTP calls made by the Flutter layer. In the checkout scenario, this covers the home screen, product list, cart screen, and order confirmation screen.

The complete sample app already contains these changes in:

```text
workshop/flutter-hybrid-rum/flutter-shop/lib/main.dart
workshop/flutter-hybrid-rum/flutter-shop/lib/src/rum_service.dart
```

The exact package version can change, so use the current version from the Splunk guided setup or from `pub.dev`.

{{% notice title="Exercise" style="green" icon="running" %}}

From the root of your Flutter app, add the package:

```bash
flutter pub add splunk_otel_flutter
flutter pub get
```

Check the platform requirements in the current package documentation. At the time this workshop was written, the package required recent Flutter and Dart SDKs, Android API level 24 or higher, and iOS 15 or higher.

For Android, confirm your app module enables core library desugaring and sets a supported `minSdkVersion`.

For iOS, confirm Swift Package Manager is enabled for the Flutter project:

```bash
flutter config --enable-swift-package-manager
```

{{% /notice %}}

## Initialize the Agent

Install RUM before `runApp()` so startup and navigation data are captured consistently. This is the first instrumentation point in the app:

```text
main()
  -> initialize Flutter bindings
  -> install Splunk RUM
  -> attach shared app context
  -> runApp()
```

After this change, the Flutter agent can emit telemetry for the mobile shell without every screen needing its own instrumentation code.

{{% notice title="Exercise" style="green" icon="running" %}}

Use the reference implementation in `workshop/flutter-hybrid-rum/flutter/main.dart` and adapt it to your app:

```dart
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
  );

  runApp(const MyApp());
}
```

Build with values supplied from your environment:

```bash
flutter run \
  --dart-define=SPLUNK_RUM_REALM="$SPLUNK_RUM_REALM" \
  --dart-define=SPLUNK_RUM_ACCESS_TOKEN="$SPLUNK_RUM_ACCESS_TOKEN" \
  --dart-define=SPLUNK_RUM_APPLICATION_NAME="$SPLUNK_RUM_APPLICATION_NAME" \
  --dart-define=SPLUNK_RUM_ENVIRONMENT="$SPLUNK_RUM_ENVIRONMENT" \
  --dart-define=SPLUNK_RUM_APP_VERSION="$SPLUNK_RUM_APP_VERSION"
```

Open the app and move through two or three screens that make network requests.

{{% /notice %}}

## What This Change Adds

With only the initialization step, the app starts sending telemetry with:

- The RUM application name, such as `mobile-checkout`.
- The deployment environment, such as `workshop`.
- The app version, such as `1.0.0`.
- Mobile device and platform context.
- Flutter lifecycle and navigation signals supported by the agent.
- Network request timing for covered mobile HTTP paths.

The next section adds business context so those raw technical signals become useful during troubleshooting.

{{% notice title="Token handling" style="info" %}}
RUM access tokens are intended for client-side telemetry ingestion, but they are still configuration values. Keep them out of screenshots, public repositories, crash reports, and unrelated logs.
{{% /notice %}}

## Optional Modules

The Flutter package supports module configuration for features such as navigation, interactions, crash reports, slow rendering, and Android ANR reporting. Start with the default path, then explicitly configure modules when you need to control sampling, feature availability, or rollout risk.

{{< tabs >}}
{{% tab title="Question" %}}
**Why should you install RUM before `runApp()`?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Startup and early navigation happen before the first screen settles. Installing first gives the agent the best chance to capture the full app lifecycle.**
{{% /tab %}}
{{< /tabs >}}
