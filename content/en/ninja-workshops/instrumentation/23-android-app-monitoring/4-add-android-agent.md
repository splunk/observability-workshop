---
title: 4. Add the Android Agent
weight: 4
time: 15 minutes
description: Add Maven Central, desugaring, and the Splunk RUM Android dependency to the app.
---

In this module you will add the Splunk RUM Android agent dependency and make sure the
Android build can run the APIs used by the agent.

## Add Maven Central

Confirm that your project repositories include Maven Central.

```kotlin
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
```

Older projects might use `allprojects` in the root `build.gradle` instead:

```kotlin
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
```

## Enable Java 8 Compatibility and Desugaring

In the application module, enable Java 8 compatibility and core library desugaring.

```kotlin
android {
    compileOptions {
        isCoreLibraryDesugaringEnabled = true
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }

    kotlinOptions {
        jvmTarget = "1.8"
    }
}
```

Add the desugaring dependency:

```kotlin
dependencies {
    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.3")
}
```

## Add the Splunk RUM Dependency

Add the agent dependency to the app module.

```kotlin
dependencies {
    implementation("com.splunk:splunk-otel-android:2.3.1")
}
```

Use a pinned version. Do not use a `+` wildcard for production builds.

## Optional: Add Automatic Network Instrumentation Plugins

If the app uses OkHttp3 or `HttpURLConnection` and you want build-time automatic
network request instrumentation, add the matching Gradle plugin to the app module.

```kotlin
plugins {
    id("com.splunk.rum-okhttp3-auto-plugin") version "2.3.1"
    id("com.splunk.rum-httpurlconnection-auto-plugin") version "2.3.1"
}
```

Use only the plugins that match HTTP clients used by your app. You will configure the
matching runtime module settings in the next exercises.

{{% notice title="Current Version" style="info" %}}
The example uses `2.3.1` because the Splunk Android SDK repository listed it as the
latest release when this workshop was written. If the official onboarding page for
your organization shows a newer supported version, use that version consistently for
the SDK and related Gradle plugins.
{{% /notice %}}

## Remove Duplicate OpenTelemetry Android Instrumentation

If your app already has this dependency, remove it:

```kotlin
implementation("io.opentelemetry.android:instrumentation:2.0.0")
```

The Splunk SDK already includes the upstream Android instrumentation it needs. Keeping
both can cause duplicate class or AAR metadata failures.

## Sync and Build

Sync the project in Android Studio, then run:

```bash
./gradlew :app:assembleDebug
```

Replace `:app` with your application module name if it differs.

## Exercise

Before continuing, verify:

- Gradle sync succeeds.
- The debug APK builds.
- No duplicate OpenTelemetry Android dependency remains.
- Your app still launches without calling `SplunkRum.install()` yet.
- Any automatic network instrumentation plugins match HTTP clients your app actually
  uses.
