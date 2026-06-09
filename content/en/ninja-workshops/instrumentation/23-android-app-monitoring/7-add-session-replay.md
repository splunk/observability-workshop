---
title: 7. Add Session Replay
weight: 7
time: 10 minutes
description: Optionally enable Android session replay with privacy controls.
---

Session replay can make mobile troubleshooting much faster, but it should be enabled
only after product, legal, privacy, and security expectations are clear. This module is
optional for the workshop.

{{% notice title="Privacy Review" style="warning" %}}
You are responsible for providing required notices and consent for data collected from
users. Mask sensitive data before starting recordings, and validate replay output with
test accounts before a production rollout.
{{% /notice %}}

## Start Recording

Enable the session replay module during RUM initialization:

```kotlin
import com.splunk.rum.integration.sessionreplay.SessionReplayModuleConfiguration

SplunkRum.install(
    application = this,
    agentConfiguration = agentConfiguration,
    moduleConfigurations = arrayOf(
        SessionReplayModuleConfiguration(
            isEnabled = true,
            samplingRate = 0.2f
        )
    )
)
```

Then start session replay after the RUM agent has been initialized:

```kotlin
import com.splunk.rum.integration.sessionreplay.extension.sessionReplay

SplunkRum.instance.sessionReplay.start()
```

The `sessionReplay` module publishes replay chunks periodically. It stops when the app
goes to the background and resumes when the app returns to the foreground if recording
was active.

## Stop Recording

If you need an explicit opt-out or a high-sensitivity workflow, stop recording:

```kotlin
import com.splunk.rum.integration.sessionreplay.extension.sessionReplay

SplunkRum.instance.sessionReplay.stop()
```

## Choose a Rendering Mode

Use wireframe mode when you want interaction context without recording rendered user
content.

```kotlin
import com.splunk.rum.integration.sessionreplay.api.RenderingMode
import com.splunk.rum.integration.sessionreplay.extension.sessionReplay

val preferences = SplunkRum.instance.sessionReplay.preferences
preferences.renderingMode = RenderingMode.WIREFRAME_ONLY
```

Use native mode only when the app has passed privacy review and masking validation.

## Mask Sensitive UI

For Jetpack Compose, mark sensitive elements:

```kotlin
import com.splunk.rum.integration.sessionreplay.api.sessionReplay

Text(
    text = "Card number",
    modifier = Modifier.sessionReplay(isSensitive = true)
)
```

For XML views, mark a view instance:

```kotlin
import com.splunk.rum.integration.sessionreplay.api.isSensitive

paymentCardNumberView.isSensitive = true
```

The session replay documentation also supports recording masks when a rectangular
region must be hidden.

## Exercise

Enable session replay in a debug build, then:

1. Start recording only after consent or a workshop-only debug control.
2. Navigate through a simple workflow.
3. Confirm sensitive inputs are hidden.
4. Stop recording.
5. In Splunk RUM, open the session and confirm replay metadata appears.

If sensitive data is visible, disable replay and fix masking before continuing.
