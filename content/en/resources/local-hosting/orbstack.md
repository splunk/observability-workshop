---
title: Local Hosting with OrbStack
weight: 2
description: Learn how to create a local hosting environment with OrbStack - Mac (Apple Silicon)
---

Install Orbstack:

``` bash
brew install orbstack
```

Log Observer Connect:

If you plan to use your own Splunk Observability Cloud Suite Org and or Splunk instance, you may need to create a new **Log Observer Connect** connection:
Follow the instructions found in the [documentation](https://docs.splunk.com/observability/en/logs/lo-connect-landing.html) for [Splunk Cloud](https://docs.splunk.com/observability/en/logs/scp.html#logs-scp) or [Splunk Enterprize](https://docs.splunk.com/observability/en/logs/set-up-logconnect.html).

Additional requirements for running your own **Log Observer Connect** connection are:
Create an index called **splunk4rookies-workshop**
Make sure the Service account user used in the **Log observer Connect** Connection has access to the **splunk4rookies-workshop** index. (You can remove all other indexes, as all workshop log data should go to this index)

Clone workshop repository:

``` bash
git clone https://github.com/splunk/observability-workshop
```

Change into Orbstack directory:

```bash
cd observability-workshop/local-hosting/orbstack
```

Copy the `start.sh.example` to `start.sh` and edit the file to set the following required variables
Make sure  that you do not use a Raw Endpoint, but use an Event Endpoint instead as this will process the logs correctly

- `ACCESS_TOKEN`
- `REALM`
- `API_TOKEN`
- `RUM_TOKEN`
- `HEC_TOKEN`
- `HEC_URL`

Run the script and provide and instance name e.g.:

``` bash
./start.sh my-instance
```

Once the instance has been successfully created (this can take several minutes), you will automatically be logged into the instance. If you exit you can SSH back in using the following command (replace `<my_instance>` with the name of your instance):

```bash
ssh splunk@<my_instance>@orb
```

Once in the shell, you can validate that the instance is ready by running the following command:

```bash
kubectl version --output=yaml
```

To get the IP address of the instance, run the following command:

```bash
ifconfig eth0
```

To delete the instance, run the following command:

```bash
orb delete my-instance
```
