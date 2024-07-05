---
title: Local Hosting with OrbStack
weight: 2
draft: false
---

## Preparing an Orbstack instance

**NOTE:** Please disable any VPNs or proxies before running the commands below e.g:

- ZScaler
- Cisco AnyConnect

These tools **will** prevent the instance from being created properly.

## 1. Pre-requisites

Install Orbstack:

``` bash
brew install orbstack
```

## 2. Clone workshop repository

``` bash
git clone https://github.com/splunk/observability-workshop
```

## 3. Change into Orbstack directory

```bash
cd observability-workshop/local-hosting/orbstack
```

## 4. Create start.sh script

Copy the `start.sh.example` to `start.sh` and edit the file to set the required variables:

- ACCESS_TOKEN
- REALM
- API_TOKEN
- RUM_TOKEN
- HEC_TOKEN
- HEC_URL

Run the script and provide an instance name e.g.: `./start.sh my-instance`.

Once the instance has been successfully created (this can take several minutes), you will automatically be logged into the instance. If you exit you can SSH back in using the following command:

```bash
ssh splunk@<my_instance>@orb
```

## 5. Validate instance

Once in the shell, you can validate that the instance is ready by running the following command:

```bash
kubectl version --output=yaml
```

To get the IP address of the instance, run the following command:

```bash
ifconfig eth0
```

If you get an error please check that you have disabled any VPNs or proxies and try again e.g. ZScaler, Cisco AnyConnect.

To start again, delete the instance and re-run `start.sh my-instance`:

```bash
orb delete my-instance
```
