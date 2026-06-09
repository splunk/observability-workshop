# Flutter and Hybrid RUM Workshop Support Files

This folder contains small reference snippets for the workshop at:

```text
content/en/ninja-workshops/instrumentation/22-flutter-hybrid-rum/
```

The workshop assumes you bring an existing Flutter, WebView, Capacitor, Cordova, Ionic, or mixed mobile app. These snippets are not a complete sample application. They model a mobile checkout app where Flutter owns app launch, product browsing, cart, and confirmation, while a WebView can own checkout, promo, help, identity, or terms content.

The app behavior already exists before the workshop starts:

```text
Launch app -> browse products -> add to cart -> open WebView checkout -> confirm order
```

The workshop does not change checkout behavior. It adds telemetry around the behavior so Splunk can show the user session, Flutter screens, WebView activity, network calls, and backend traces.

Instrumentation is added in three places:

- `flutter/main.dart` installs Flutter RUM before `runApp()` and adds mobile app context.
- `hybrid/rum-bootstrap.js` initializes browser RUM inside the WebView's JavaScript runtime.
- `apm/server-timing.md` documents the backend headers and APM setup needed to connect front-end sessions to server-side traces.

## Files

| Path | Purpose |
| ---- | ------- |
| `.env.example` | Local workshop values for realm, token, app name, environment, and app version. |
| `flutter/main.dart` | Minimal Flutter RUM initialization and context examples. |
| `hybrid/rum-bootstrap.js` | Browser RUM bootstrap pattern for embedded WebView/hybrid content. |
| `hybrid/webview-config.html` | Example configuration block for server-rendered or injected WebView settings. |
| `apm/server-timing.md` | Backend checklist for RUM-to-APM correlation. |

## Suggested Lab Flow

1. Copy `.env.example` to `.env` and fill in non-production values.
2. Load the values into your shell:

```bash
set -a
source .env
set +a
```

3. Add the current `splunk_otel_flutter` package to your Flutter app.
4. Adapt `flutter/main.dart` to your app's initialization path.
5. If your app uses WebView content, add browser RUM to the web bundle using `hybrid/rum-bootstrap.js`.
6. Generate sessions from a simulator or real device.
7. Validate the sessions in Splunk RUM and check APM correlation for backend calls.

Do not commit real RUM tokens.
