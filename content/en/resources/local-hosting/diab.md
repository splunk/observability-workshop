---
title: Running Demo-in-a-Box
weight: 3
description: Learn how to use Demo-in-a-Box to manage demos and otel collectors in an easy-to-use web interface
---

**Demo-in-a-box** is a method for running demo apps easily using a web interface.

It provides:
* A quick way to deploy demo apps and states
* A way to easily change configuration of your otel collector and see logs
* Get pod status, pod logs, etc.

To leverage this locally using multipass:
* Follow the [local hosting for multipass](../multipass) instructions
  * In the `terraform.tfvars` file, set `splunk_diab` to `true`
  * Then set the other required and important tokens/url
  * Then run the terraform steps
* Once the instance is up, navigate in your browser to: `http://<IP>:8083`
  * If the instance isn't up or has errors you can try changing the `wsversion` from a version number to `main`
    * This will pull the latest development version
    * You can also try an older version number
    * After making the change, run `terraform apply` to make the changes
* Now you can deploy any of the demos; this will also deploy the collector