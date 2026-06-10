# Flutter Hybrid RUM Shop

This is a runnable sample app for the Flutter and hybrid RUM workshop. It models a small mobile commerce flow:

```text
Launch app -> browse products -> add to cart -> open WebView checkout -> confirm order
```

The app demonstrates three instrumentation boundaries:

- Flutter RUM in `lib/main.dart` and `lib/src/rum_service.dart`.
- Custom Flutter events and workflows around product, cart, and checkout actions.
- Browser RUM inside `assets/web/checkout.html`, loaded by the WebView checkout screen.

## Requirements

- Flutter SDK 3.32 or later.
- Dart SDK 3.8 or later.
- Android API level 24 or later, or iOS 15 or later.
- A Splunk Observability Cloud realm and RUM access token for live telemetry.

Flutter is not vendored in this repo. Generate the platform folders on a machine with Flutter installed:

```bash
cd workshop/flutter-hybrid-rum/flutter-shop
./scripts/bootstrap-platforms.sh
```

## Run Without Live RUM

The app runs with placeholder values and disables live RUM export. This is useful when explaining the app flow before giving attendees a token.

```bash
flutter run
```

## Run With Live RUM

Load workshop values from the parent folder:

```bash
cd workshop/flutter-hybrid-rum
cp .env.example .env
set -a
source .env
set +a
```

Run the sample:

```bash
cd flutter-shop
flutter run \
  --dart-define=SPLUNK_RUM_REALM="$SPLUNK_RUM_REALM" \
  --dart-define=SPLUNK_RUM_ACCESS_TOKEN="$SPLUNK_RUM_ACCESS_TOKEN" \
  --dart-define=SPLUNK_RUM_APPLICATION_NAME="$SPLUNK_RUM_APPLICATION_NAME" \
  --dart-define=SPLUNK_RUM_ENVIRONMENT="$SPLUNK_RUM_ENVIRONMENT" \
  --dart-define=SPLUNK_RUM_APP_VERSION="$SPLUNK_RUM_APP_VERSION" \
  --dart-define=SPLUNK_RUM_HYBRID_APPLICATION_NAME="$SPLUNK_RUM_HYBRID_APPLICATION_NAME"
```

## What to Click

1. Open the app and check the telemetry status on the first screen.
2. Tap **View** on a product, then **Add to cart**.
3. Open the cart and tap **Start checkout**.
4. In the WebView checkout page, tap **Calculate shipping**, then **Complete checkout**.
5. Return to Splunk RUM and filter by the application name and environment.

## Instrumentation Map

| App behavior | File | Instrumentation |
| ------------ | ---- | --------------- |
| App startup | `lib/main.dart` | Installs `splunk_otel_flutter` before `runApp()`. |
| Shared app tags | `lib/src/rum_service.dart` | Sets app version, shell, build flavor, and tenant tier attributes. |
| Product view | `lib/src/screens/product_detail_screen.dart` | Tracks manual screen view and product viewed event. |
| Add to cart | `lib/src/shop_store.dart` | Tracks `cart_item_added`. |
| Checkout duration | `lib/src/shop_store.dart` | Starts and ends a `checkout` workflow. |
| Embedded checkout | `assets/web/checkout.html` | Initializes browser RUM for WebView JavaScript. |
| Backend calls | `lib/src/shop_api.dart` and WebView `fetch()` calls | Creates mobile and WebView network requests for RUM/APM validation. |

## Notes

- The default backend target is `https://httpbin.org` so the app can create real HTTP requests without a local server.
- Set `SHOP_API_BASE_URL` with `--dart-define` to point at your own instrumented backend.
- Do not commit real RUM tokens.
