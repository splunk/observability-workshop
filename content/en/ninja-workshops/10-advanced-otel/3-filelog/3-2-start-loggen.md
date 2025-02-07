---
title: 3.2 Start Log-Gen
linkTitle: 3.2 Start Log-Gen
weight: 2
---

{{% notice title="Exercise" style="green" icon="running" %}}

Start the appropriate script for your system. The script will begin writing lines to a file named `quotes.log`:

```sh { title="Log Generator" }
./log-gen.sh
```

```text { title="Log Generator Output" }
Writing logs to quotes.log. Press Ctrl+C to stop.
```

{{% notice note %}}
On Windows, you may encounter the following error:

{{% textcolor color=red %}}
.\log-gen.ps1 : File .\log-gen.ps1 cannot be loaded because running scripts is disabled on this system ...
{{% /textcolor %}}

To resolve this run:

```ps1
powershell -ExecutionPolicy Bypass -File log-gen.ps1
```

{{% /notice %}}
{{% /notice %}}
