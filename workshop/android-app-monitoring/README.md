# Android App Monitoring Sample

This is the runnable Android sample app for the **Android App Monitoring with Splunk
RUM** workshop.

The app is a small native Android shopping flow called **Buttercup**. It runs in an
Android emulator and demonstrates where Splunk RUM instrumentation is added:

- `InstrumentedShopApplication.java` initializes Splunk RUM in `Application.onCreate()`.
- `MainActivity.java` tracks screen navigation, custom events, workflow spans, handled
  exceptions, and instrumented OkHttp calls.
- `app/build.gradle.kts` injects the Splunk realm, RUM token, app name, and environment
  into `BuildConfig`.

## Prerequisites

- Android Studio or Android SDK command-line tools.
- Android SDK platform 34 or higher.
- A running Android emulator or connected Android device.
- A Splunk Observability Cloud realm and RUM access token.

## Build Without Sending RUM Data

The app can build and run without a token. In that mode, RUM uses no-op instrumentation
and the UI still shows where each signal would be emitted.

```bash
cd workshop/android-app-monitoring
ANDROID_HOME="$HOME/Library/Android/sdk" ./gradlew :app:assembleDebug
```

## Install With Splunk RUM Enabled

Pass workshop values as Gradle properties:

```bash
cd workshop/android-app-monitoring

ANDROID_HOME="$HOME/Library/Android/sdk" ./gradlew :app:installDebug \
  -PsplunkRealm=us1 \
  -PsplunkRumAccessToken=replace-with-rum-token \
  -PsplunkRumAppName=buttercup-android \
  -PsplunkRumEnvironment=workshop
```

Then launch the app from the emulator. Use the buttons in this order:

1. **Open product detail**
2. **Add item to cart**
3. **Enter shipping**
4. **Submit checkout**
5. **Track handled payment error**

The app writes an on-screen instrumentation log and sends telemetry when a valid RUM
token is supplied.

## What To Look For In Splunk RUM

Filter to:

- Application: `buttercup-android`
- Environment: `workshop`
- Version: `1.0.0-workshop`

Expected signals:

- Screen navigation: `product_list`, `product_detail`, `cart`,
  `checkout_shipping`, `checkout_payment`, `confirmation`
- Custom events: `product_detail_viewed`, `cart_item_added`,
  `checkout_step_viewed`
- Workflow span: `checkout_submit`
- Handled exceptions for catalog, checkout, or payment failures
- OkHttp network calls to `https://httpbin.org/json` and
  `https://httpbin.org/delay/1`

## Important Files

```text
app/src/main/java/com/splunk/workshop/androidrum/InstrumentedShopApplication.java
app/src/main/java/com/splunk/workshop/androidrum/MainActivity.java
app/build.gradle.kts
```
