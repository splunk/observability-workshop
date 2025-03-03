---
title: 7.2 Setup Environment
linkTitle: 7.2 Setup Environment
weight: 2
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Log Generator**:  

1. Open the **Test** terminal window and navigate to the `[WORKSHOP]/7-transform-data` directory.  
2. Run the `log-gen` script for your system.  
   - **Important**: To ensure the logs are structured in JSON format, include the `-json` flag when starting the script.  

```sh { title="Log Generator" }
./log-gen.sh -json
```

The script will begin writing lines to a file named `./quotes.log`, while displaying a single line of output in the console.

```txt { title="Log Generator Output" }
Writing logs to quotes.log. Press Ctrl+C to stop.
```

**Start the Gateway**: In the **Gateway** terminal window navigate to the `[WORKSHOP]/7-transform-data` directory and run:

```sh { title="Gateway" }
../otelcol --config=gateway.yaml
```

**Start the Agent**: In the **Agent** terminal window navigate to the `[WORKSHOP]/7-transform-data` directory and run:

```sh { title="Agent" }
../otelcol --config=agent.yaml
```

{{% /notice %}}
