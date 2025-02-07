---
title: 7.2 Setup Environment
linkTitle: 7.2 Setup Environment
weight: 2
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Log Generator**: In the **Test** terminal window, navigate to the `[WORKSHOP]/7-transform-data` directory and start the appropriate `log-gen` script for your system. We want to work with structured JSON logs, so add the `-json` flag.

```sh
./log-gen.sh -json
```

The script will begin writing lines to a file named `./quotes.log`, while displaying a single line of output in the console.

```txt
Writing logs to quotes.log. Press Ctrl+C to stop.
```

**Start the Gateway**: In the **Gateway** terminal window navigate to the `[WORKSHOP]/7-transform-data` directory and run:

```sh
../otelbin --config=gateway.yaml
```

**Start the Agent**: In the **Agent** terminal window navigate to the `[WORKSHOP]/7-transform-data` directory and run:

```sh
../otelbin --config=agent.yaml
```

{{% /notice %}}
