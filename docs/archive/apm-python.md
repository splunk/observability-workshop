## Step 1: Infrastructure setup complete, now let’s run our first fully monitored application!
1. Switch to the Application instance (the one created in Lab #1) and change to the mypythonapp directory
   ```bash
   cd ~/mypythonapp
   ```

2. In order to see how the demonstration Python application has been instrumented using https://github.com/signalfx/signalfx-python-tracing type `more demo.py`
   ```python
   #!/usr/bin/env python

   from flask import Flask, make_response, request
   from signalfx_tracing import trace
   import opentracing

   app = Flask(__name__)

   @trace
   def convert_response(message):
     # In this example we want to force this trace to be retained
     opentracing.tracer.active_span.set_tag('sampling.priority', 1)
     opentracing.tracer.active_span.set_tag('message', message)
     print(opentracing.tracer.active_span)
     return 'You said: {}'.format(message)

   @app.route('/echo', methods=['POST'])
   def echo():
     message = request.data.decode('utf-8')
     return make_response(convert_response(message))

   if __name__ == '__main__':
     app.run()
   ```

3. Start the Python application by running the following command, replace `[YOUR_INITIALS]` to make your application unique.
   ```bash
   SIGNALFX_SERVICE_NAME=[YOUR_INITIALS]-app-dev-python-app sfx-py-trace ./demo.py & disown
   ```

   **IMPORTANT:** After running this code, hit the enter key in your keyboard to get out of the process and continue with the following steps. Don't worry, your python app will continue running in the background.

---
## Step 2: Generate some Traces
1. We will be using a really practical tool to simulate requests called Apache Benchmark or ab. But first let's make sure that the service we started before can actually accept requests, by running the following command:
   ```bash
   curl -XPOST -d'Hello, world' -H'Content-Type:text/plain' http://localhost:5000/echo
   ```

   You should get something like:
   ```bash
   795cf220f0ee0afa:7a1f10140ad14024:4a81cc4098335da:3 rwc-app-dev-python-app.convert_response
   127.0.0.1 - - [04/Nov/2019 15:07:24] "POST /echo HTTP/1.1" 200 -
   ```

   If you don't get this response, make sure the Step #1.2 (above) was executed properly and that you have a service running called `./demo.py` executed by python. On the Application instance itself you can confirm this by running `ps -ef | grep demo.py`

2. Now that we know we can call our service, let's run ab to simulate load and start generating traces that our Smart Gateway can capture and send to the SignalFx platform. Confirm a file named `~/mypythonapp/post_data.json` exists and has the following inside:
   ```
   "Hello from the App Dev Workshop!"
   ```

3. Save the file, and in the same directory, execute the following:
   ```bash
   ab -p post_data.json -T application/json -c20 -n1000 http://localhost:5000/echo
   ```

   This will create 20 concurrent connections to our localhost python app, and it will post the data 1000 times.

---
## Step 3: Visualizing the Data
1. Over in SignalFx, under the Built-In Dashboard Groups, you will see a Smart Gateway Dashboard group. Go to the Cluster(s) Dashboard:


2. Over there you will see information about the host running the Smart Gateway, and a few other numbers that are important. But the most important of all, are the 3 big number group of charts, showing TAPM, Retained TPM and APM Identities.

   * **TAPM** are the Traces Analysed Per Minute, which is the amount of traces that the Smart Gateway is ingesting and processing.

   * **Retained TPM** are the traces that the Smart Gateway, after processing them, think are important to keep, and send to SignalFx for further analysis by the users.

   * **APM Identities** are each unique span and initiating span/endpoint tracked by the Smart Gateway and sent to SignalFx. To explain this a little better please see the following image:


   If you want to know more about Traces, Spans, Metrics and Metadata, please follow this link. If everything goes according to plan, you should see in that dashboard, some numbers that represent the test we just did.

---
## Step 4: Analyzing Traces
1. Navigate to uAPM → Traces on the main toolbar, then ensure you have selected your cluster from the Cluster dropdown at the top left, you should see something like this:

2. Feel free to investigate our built-in Outlier Analysis, showing the potential source of our problems in our application, or navigate to some of the traces, and inspect the payload we sent in our test.
You go to a trace by clicking on it:

   Then click on the span that handled the response, and see the message:

3. Feel free to continue navigating uAPM features now that we have traces and spans going in.
Also, you can try sending more tests or changing the payload of the tests to see how fast the new tests are ingested and analyzed in SignalFx.


4. Once you finish, please proceed to [Lab 3: Simple Java auto-instrumentation](https://github.com/signalfx/app-dev-workshop/wiki/Module-2-Lab-3:-Simple-Java-auto-instrumentation)
