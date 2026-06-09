---
title: 5. Initialize and Configure RUM
weight: 5
time: 20 minutes
description: Initialize the Splunk RUM Android agent from the Application class.
---

Initialize RUM once, as early as practical in your application lifecycle. The usual
place is `Application.onCreate()`.

## What This Step Changes

Before this module, Buttercup is just a normal Android app. It launches screens and
calls APIs, but Splunk has no visibility into the user's mobile session.

After this module, the app starts the Splunk RUM agent during process startup. From
that point forward, the SDK can observe app lifecycle events, rendering signals,
crashes, ANRs, interactions, and configured network activity. Later modules add the
manual names and business context that make those signals easier to interpret.

## Add an Application Class

If your project does not already have a custom `Application` class, create one:

```kotlin
package com.example.buttercup

import android.app.Application
import com.splunk.rum.integration.agent.api.AgentConfiguration
import com.splunk.rum.integration.agent.api.EndpointConfiguration
import com.splunk.rum.integration.agent.api.SplunkRum

class ButtercupApplication : Application() {
    override fun onCreate() {
        super.onCreate()

        SplunkRum.install(
            application = this,
            agentConfiguration = AgentConfiguration(
                endpoint = EndpointConfiguration(
                    realm = BuildConfig.SPLUNK_REALM,
                    rumAccessToken = BuildConfig.SPLUNK_RUM_ACCESS_TOKEN
                ),
                appName = BuildConfig.SPLUNK_RUM_APP_NAME,
                deploymentEnvironment = BuildConfig.SPLUNK_RUM_ENVIRONMENT,
                appVersion = BuildConfig.VERSION_NAME
            )
        )
    }
}
```

Register the class in `AndroidManifest.xml`:

```xml
<application
    android:name=".ButtercupApplication"
    ...>
</application>
```

## What Each Configuration Value Means

| Value | Purpose |
| --- | --- |
| `realm` | Routes telemetry to the correct Splunk Observability Cloud realm. |
| `rumAccessToken` | Allows the mobile app to send RUM telemetry. |
| `appName` | Groups sessions under the mobile application in RUM. |
| `deploymentEnvironment` | Separates `dev`, `qa`, `prod`, and workshop traffic. |
| `appVersion` | Lets teams compare releases and investigate version-specific crashes. |
| `enableDebugLogging` | Prints SDK diagnostics while validating the setup. |

## Add Debug Logging for the First Run

For the workshop, temporarily enable debug logging:

```kotlin
AgentConfiguration(
    endpoint = EndpointConfiguration(
        realm = BuildConfig.SPLUNK_REALM,
        rumAccessToken = BuildConfig.SPLUNK_RUM_ACCESS_TOKEN
    ),
    appName = BuildConfig.SPLUNK_RUM_APP_NAME,
    deploymentEnvironment = BuildConfig.SPLUNK_RUM_ENVIRONMENT,
    appVersion = BuildConfig.VERSION_NAME,
    enableDebugLogging = true
)
```

Turn debug logging off before production release.

## Optional: Support API Levels 21-23

By default, the Splunk RUM Android 2.x agent runs on API level 24 and higher. If your
app must collect data on API levels 21-23, test with lower API emulators and configure
lower API support:

```kotlin
AgentConfiguration(
    endpoint = EndpointConfiguration(
        realm = BuildConfig.SPLUNK_REALM,
        rumAccessToken = BuildConfig.SPLUNK_RUM_ACCESS_TOKEN
    ),
    appName = BuildConfig.SPLUNK_RUM_APP_NAME,
    deploymentEnvironment = BuildConfig.SPLUNK_RUM_ENVIRONMENT,
    forceEnableOnLowerApi = true
)
```

Only keep this setting if your app passes lower API smoke tests.

## Add Low-Cardinality Global Context

Use stable, low-cardinality values for app-wide context. Do not add user email,
session IDs, account names, or raw device identifiers as metric dimensions.

Good examples:

| Attribute | Example |
| --- | --- |
| `app.release_channel` | `internal` |
| `business.unit` | `retail` |
| `feature.branch` | `checkout-v2` |

Keep high-cardinality and personally identifiable information out of spans unless your
privacy and retention policy explicitly allows it.

## Run the App

Start the app on an emulator or device:

```bash
./gradlew :app:installDebug
```

Open Logcat and filter for Splunk or OpenTelemetry messages. Then use the app for a
minute so the agent has lifecycle and interaction data to send.

## Exercise

Confirm:

- The application launches with `SplunkRum.install()` enabled.
- Logcat does not show initialization errors.
- The app name, environment, and version are the values you expected.
- Debug logging is enabled only for this lab run.
