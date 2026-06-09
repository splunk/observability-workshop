---
title: 7. Upload dSYMs
linkTitle: 7. Upload dSYMs
weight: 7
---

RUM can capture mobile crashes, but crash reports are only useful when stack traces are symbolicated. In this lab you upload dSYMs for the exact app build.

## Install the CLI

Install the `splunk-rum` CLI on the build machine:

```bash
npm install @splunk/rum-cli --global
```

Set organization-level authentication for the CLI:

```bash
export SPLUNK_REALM=us1
export SPLUNK_ACCESS_TOKEN=replace-with-your-org-api-token
```

Use an organization API access token with the required scope and role. Do not use the RUM access token for dSYM upload.

## Build with dSYMs

Confirm release builds use:

```text
DEBUG_INFORMATION_FORMAT = dwarf-with-dsym
```

Archive the app in Xcode or in CI, then locate the generated `dSYMs/` directory in the archive package.

## Upload dSYMs

Upload the directory:

```bash
splunk-rum ios upload --path path-to-dSYMs
```

Verify the upload:

```bash
splunk-rum ios list
```

The supporting script wraps those commands:

```text
workshop/mobile-rum-dxa-ios/scripts/upload-dsyms.sh
```

Example:

```bash
SPLUNK_REALM=us1 \
SPLUNK_ACCESS_TOKEN=replace-with-your-org-api-token \
DSYM_PATH="/path/to/MyApp.xcarchive/dSYMs" \
workshop/mobile-rum-dxa-ios/scripts/upload-dsyms.sh
```

## CI checklist

- Upload dSYMs before distributing the matching binary.
- Upload dSYMs from the main app and third-party frameworks when available.
- Store `SPLUNK_ACCESS_TOKEN` in CI secrets, not in the repository.
- Fail the release job when upload fails for production builds.
- Keep the app version in RUM aligned with the released binary version.

{{% notice title="Retention note" style="info" %}}
Splunk RUM stores uploaded dSYMs permanently. Treat uploads as release artifacts and avoid uploading incorrect or unrelated archives.
{{% /notice %}}
