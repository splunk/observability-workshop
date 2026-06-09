---
title: 3. Add the iOS RUM Agent
linkTitle: 3. Add Agent
weight: 3
---

In this lab you add the Splunk RUM iOS agent to the app through Swift Package Manager and initialize it early in app startup. The included app already has a training instrumentation layer, so the task is to connect those same app hook points to Splunk RUM.

## Add the package

In Xcode:

1. Open the application project.
2. Select **File > Add Packages**.
3. Enter the package URL:

```text
https://github.com/signalfx/splunk-otel-ios
```

4. Select the `SplunkAgent` package.
5. Add it to the app target.

For production apps, test the latest package in pre-production, then pin a tested version for release builds. Keep production updates on a regular cadence instead of floating every build to `latest`.

## What code you are adding

The RUM package does not change the app flow by itself. You add one bootstrap function that runs at startup. That function:

1. builds an endpoint configuration from the Splunk realm and RUM token,
2. builds an agent configuration with the app name and environment,
3. installs RUM once for the process,
4. turns on automatic screen navigation tracking,
5. starts Session Replay when the app is ready to record,
6. leaves the rest of the app code unchanged until you add custom journey events later.

After bootstrap, the agent can automatically observe app starts, navigation, network activity, crashes, slow rendering signals, and replay frames. The later labs add the business context that automatic instrumentation cannot infer by itself.

In the training app, compare this Splunk bootstrap to:

```text
InstrumentedShop/InstrumentedShop/WorkshopStore.swift
InstrumentedShop/InstrumentedShop/Instrumentation/TrainingRumInstrumentation.swift
```

`WorkshopStore.bootstrapIfNeeded()` is the app lifecycle hook. `TrainingRumInstrumentation.start(...)` is the local stand-in for the real `SplunkRum.install(...)` call.

## Add bootstrap code

Add a bootstrap file to the app target. The supporting example is:

```text
workshop/mobile-rum-dxa-ios/Sources/RUMBootstrap.swift
```

The core initialization pattern is:

```swift
import SplunkAgent

let endpointConfiguration = EndpointConfiguration(
    realm: "YOUR_REALM",
    rumAccessToken: "YOUR_RUM_ACCESS_TOKEN"
)

let agentConfiguration = AgentConfiguration(
    endpoint: endpointConfiguration,
    appName: "YOUR_APP_NAME",
    deploymentEnvironment: "YOUR_DEPLOYMENT_ENVIRONMENT"
)

let agent = try SplunkRum.install(with: agentConfiguration)
agent.navigation.preferences.enableAutomatedTracking = true
agent.sessionReplay.start()
```

Call the bootstrap once, as early as possible:

| App type | Recommended place |
| --- | --- |
| SwiftUI | The `init()` of the `@main App` type. |
| UIKit app delegate | `application(_:didFinishLaunchingWithOptions:)`. |
| Scene-based UIKit app | App delegate startup, before scene setup work. |

Example SwiftUI placement:

```swift
@main
struct WorkshopShopApp: App {
    init() {
        RUMBootstrap.install()
    }

    var body: some Scene {
        WindowGroup {
            CatalogView()
        }
    }
}
```

Example UIKit placement:

```swift
func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
) -> Bool {
    RUMBootstrap.install()
    return true
}
```

## Run the app

Build and run the app in the iOS Simulator. Exercise a few screens and network requests.

Keep Xcode open. If startup fails, first check:

- the package was added to the correct target,
- the app imports `SplunkAgent`,
- the RUM token is a RUM token, not an organization API token,
- the realm matches the Splunk Observability Cloud organization,
- RUM is installed only once per process.

{{% notice title="APM note" style="info" %}}
Splunk APM is not required to instrument Splunk RUM for iOS. If backend services are instrumented later, RUM and APM can still be connected through distributed trace context and server response timing.
{{% /notice %}}
