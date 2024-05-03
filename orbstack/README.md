# Preparing an Orbstack instance

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
cd observability-workshop/orbstack
```

## 4. Create start.sh script

Copy the `start.sh.example` to `start.sh` and edit the file to set the required variables:

- ACCESS_TOKEN
- REALM
- HEC_TOKEN
- HEC_URL

``` bash

#!/bin/bash
echo "Building: $1";

# Change these values below to match your environment and safe this file as start.sh
export ACCESS_TOKEN="<redacted>"
export REALM="eu0"
export RUM_TOKEN="<redacted>"
export HEC_TOKEN="<redacted>"
#export HEC_URL="https://http-inputs-o11y-workshop-eu0.splunkcloud.com:443/services/collector/event"
export HEC_URL="https://http-inputs-o11y-workshop-us1.splunkcloud.com:443/services/collector/event"
export INSTANCE=$1

# Do not change anything below this line
orb create -c cloud-init.yaml -a arm64 ubuntu:jammy $INSTANCE
sleep 2
ORBENV=ACCESS_TOKEN:REALM:RUM_TOKEN:HEC_TOKEN:HEC_URL:INSTANCE orb -m $INSTANCE -u splunk ansible-playbook /home/splunk/orbstack.yml
echo "ssh splunk@$INSTANCE@orb"
ssh splunk@$INSTANCE@orb

```

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

You can use Vscode with your new orb/container. 
Make sure you have installed the remote ssh extension in  vscode

here is a sample  config for you ssh_config

```text
Host conf
  Hostname 127.0.0.1
  Port 32222
  User splunk@orb-1
  # replace or symlink ~/.orbstack/ssh/id_ed25519 file to change the key
  IdentityFile ~/.orbstack/ssh/id_ed25519
  # only use this key
  IdentitiesOnly yes
  ProxyCommand '/Applications/OrbStack.app/Contents/MacOS/../Frameworks/OrbStack Helper.app/Contents/MacOS/OrbStack Helper' ssh-proxy-fdpass 501
  ProxyUseFdpass yes
 ```
  