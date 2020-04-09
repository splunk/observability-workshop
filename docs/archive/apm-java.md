1. Back on your instance, extract the package, download our Java Agent and run the Echo server:
   ```
   cd ~/java-app
   curl -qsOL https://github.com/signalfx/signalfx-java-tracing/releases/download/v0.28.0-sfx8/signalfx-tracing.jar
   ./run-server.sh
   ```

2. Make a simple request:
   ```
   curl -XPOST -d'Hello, world' -H'Content-Type:text/plain' http://localhost:5000/echo
   ```

3. Because we're not doing anything specific to instruct the Smart Gateway to retain this trace, you might want to make this request a few times to make sure at least one of those traces will be sampled. You can confirm that this is happening after a few minutes by comparing the Traces Analyzed and Traces Retained charts on the Smart Gateway dashboard (filtered for your cluster).


