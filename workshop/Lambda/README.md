# Lambda APM Workshop
This is a workshop to introduce Tracing to AWS lambda's for Splunk APM

The workshop resource set exist out of several modules:

A Java spring-boot app to run locally that calls the Lambda function set
Several Lambda Microservices written in python and Node-Js & Java to simulating a real order system.

Use of Splunks Auto instrumentation libaries to get initial tracing  working
Adding logs and span tags to enrich the trace info and enable related content

The workshop documentation guiding you with adding Tracing to each of the modules

Requirements:

- A Machine where you can run the Java zero config agent
  (A workshop EC2 instance for example works well)
- Maven installed locally  one the above machine to run the Java springboot application
- AWS Account and AIM Permission to run/build Lambda's
- Base knowledge of Java, Python and/or Node-Js to follow guided development



