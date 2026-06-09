---
title: 8. Prepare Production Builds
weight: 8
time: 10 minutes
description: Upload mapping files, control privacy, and harden the Android monitoring rollout.
---

Debug builds prove that telemetry arrives. Production builds need repeatable release
controls so crashes, obfuscated stack traces, and tokens remain manageable.

## Upload R8 or ProGuard Mapping Files

If production builds are minified, upload mapping files so Splunk can de-obfuscate
stack traces. Add line number and source file preservation to your ProGuard rules:

```proguard
-keepattributes LineNumberTable,SourceFile
-renamesourcefileattribute SourceFile
```

Use the Splunk RUM Gradle plugin in CI for automatic mapping file upload and build ID
injection.

```kotlin
plugins {
    id("com.splunk.rum-mapping-file-plugin") version "2.3.1"
}

splunkRum {
    enabled = true
    realm = providers.gradleProperty("splunkRealm").get()
    apiAccessToken = providers.gradleProperty("splunkApiAccessToken").get()
    failBuildOnUploadFailure = false
}
```

Use an API access token for mapping upload in CI. Do not put that API token into the
Android app.

## Separate Debug, Test, and Production Settings

Use build variants or product flavors to separate:

- RUM app name.
- Deployment environment.
- RUM token.
- Debug logging.
- Session replay availability.
- Sampling and privacy settings.

Example naming:

| Variant | App name | Environment |
| --- | --- | --- |
| `debug` | `buttercup-android-debug` | `dev` |
| `qa` | `buttercup-android` | `qa` |
| `release` | `buttercup-android` | `prod` |

## Review Data Safety

Before production rollout, confirm:

- No PII is added to custom events, workflow names, or span attributes.
- Captured HTTP headers are explicitly approved.
- Session replay is disabled or masked by default until consent and policy are in
  place.
- Debug logging is disabled.
- Tokens are dedicated to the environment and can be rotated.
- Crash and ANR capture have been tested.
- Mapping upload runs in CI for every minified release build.

## Build a Release Candidate

Run a release build from CI or locally with CI-equivalent secrets:

```bash
./gradlew :app:assembleRelease
```

Then validate the APK or app bundle on a test device before releasing to users.

## Exercise

Update your rollout checklist with:

1. The CI job that uploads mapping files.
2. The owner who approves captured headers and custom attributes.
3. The release manager who can rotate RUM tokens.
4. The environment naming convention.
5. The go/no-go validation queries in Splunk RUM.
