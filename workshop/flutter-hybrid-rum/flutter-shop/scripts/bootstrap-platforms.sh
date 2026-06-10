#!/usr/bin/env bash
set -euo pipefail

if ! command -v flutter >/dev/null 2>&1; then
  echo "flutter was not found on PATH. Install Flutter 3.32 or later first." >&2
  exit 1
fi

cd "$(dirname "$0")/.."

flutter create . \
  --project-name flutter_hybrid_rum_shop \
  --org com.splunk.workshop \
  --platforms android,ios

flutter pub get

cat <<'MSG'

Platform folders generated.

Before running on Android, confirm android/app/build.gradle or build.gradle.kts has:
- minSdkVersion 24 or higher
- core library desugaring enabled
- com.android.tools:desugar_jdk_libs dependency

Before running on iOS, confirm the deployment target is iOS 15 or higher and Swift Package Manager is enabled:
  flutter config --enable-swift-package-manager

MSG
