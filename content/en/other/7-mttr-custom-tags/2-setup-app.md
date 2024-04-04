---
title: Setting up your Application
linkTitle: 2. Setup - App
weight: 2
---

## Environment Setup - Application

* Clone the workshop repository:

``` bash
git clone -b distributed-tracing-for-development-teams https://github.com/shabuhabs/javashop-otel.git
```

* Access the workshop directory:

``` bash
cd javashop-otel
```

* Set Environment Variables

``` bash
nano .env
```

{{% notice title="Note" style="info" %}}

* NO spaces in <your_name>
* The shop_user provides us an Environment Tag.
* To get your access token, go to your Splunk O11y UI -> Settings ->Access Tokens.
* It is assumed in this workshop that you can send traces to the org and token you are using.

{{% /notice %}}

* Set the following values:

``` ini
SHOP_USER=<your_name>
SPLUNK_ACCESS_TOKEN=<your_token>
SPLUNK_REALM=<your_realm>
```

* Save in nano with **[CTRL]-o [ENTER]**
* Exit nano with **[CTRL]-x**

## Build and Deploy Application

Let's get started by building and deploying our Application, the Splunk Instrument Shop. Run the commands below to begin and start reading ahead as your traces are coming up!

* Build the app

``` bash
./BuildAndDeploy.sh
```
