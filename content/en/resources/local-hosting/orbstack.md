---
title: Local Hosting with OrbStack
weight: 2
description: Learn how to create a local hosting environment with OrbStack - Mac (Apple Silicon)
---

Install Orbstack and jq:

``` bash
brew install orbstack jq
```

Clone workshop repository:

``` bash
git clone https://github.com/splunk/observability-workshop
```

Change into Orbstack directory:

```bash
cd observability-workshop/local-hosting/orbstack
```

Run the script and provide and instance name and [SWiPE ID](https://swipe.splunk.show) e.g.:

``` bash
./start.sh my-instance 12345678
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
