---
title: 6. Session Replay and Privacy
linkTitle: 6. Replay Privacy
weight: 6
---

Session Replay helps explain the behavior surfaced by DXA, but mobile screens can contain sensitive data. In this lab you start from a restrictive privacy posture and only reveal what is approved for troubleshooting.

## Start recording

After installing the RUM agent, start Session Replay:

```swift
SplunkRum.shared.sessionReplay.start()
```

You can inspect recording status in the app:

```swift
let recordingStatus = SplunkRum.shared.sessionReplay.state.status
```

## Mark sensitive UIKit views

Use sensitivity settings for UIKit screens:

```swift
SplunkRum.shared.sessionReplay.sensitivity[emailTextField] = true
SplunkRum.shared.sessionReplay.sensitivity[paymentContainerView] = true
```

Set a class-level sensitivity policy for reusable sensitive components:

```swift
SplunkRum.shared.sessionReplay.sensitivity[UITextField.self] = true
SplunkRum.shared.sessionReplay.sensitivity[UITextView.self] = true
```

Text fields, text views, and web views are sensitive by default. Keep that behavior unless you have a reviewed reason to change it.

## Mark sensitive SwiftUI views

For SwiftUI screens, use the Session Replay sensitivity modifier:

```swift
Text("Account balance")
    .sessionReplaySensitive()
```

For conditional sensitivity:

```swift
Text(viewModel.accountSummary)
    .sessionReplaySensitive(viewModel.containsSensitiveData)
```

## Handle WebViews

If the app renders web content in `WKWebView`, keep the web view sensitive by default. If you choose to record it, mark sensitive HTML in the page:

```html
<div class="session-replay-hide">
  This content will be hidden.
</div>

<input type="text" class="session-replay-show">
```

Inputs are hidden by default except button and submit inputs.

## Redact exported span data

Session Replay protects pixels. Span interception protects exported metadata. Use a span interceptor to remove or redact sensitive attributes before they leave the device.

The supporting example is:

```text
workshop/mobile-rum-dxa-ios/Sources/PrivacySpanInterceptor.swift
```

{{% notice title="Privacy review" style="warning" %}}
Review privacy with product, legal, and security owners before enabling Session Replay in production. The workshop examples are technical controls, not a substitute for consent, retention, or data classification policy.
{{% /notice %}}
