# Pet clinic demo

This demo will help demonstrate using call graphs. It introduces some latency to diagnose with that capability.

It assumes you are using a vm with a /home/ubuntu directory, which it will populate. Use at your own risk.

## Pre-requisites

To setup this demo, deploy the following on a linux host. It has been tested on a host with 4 CPUs, 16GB RAM, and 40GB disk, but may be able to run with less.

The scripts assume you are cloning this repo from /home/ubuntu. If you do it in a different directory you may need to adjust some of these files.

Multipass uses that setup, so this configuration was tested:

```
multipass launch -n petclinic -c 4 -m 16G -d 40G
```

## Preparation

```
cd /home/ubuntu
git clone https://github.com/splunk/observability-workshop.git
mv observability-workshop/workshop .
rm -rf observability-workshop
cd workshop/demos/petclinic-demo
```

## One time Setup

```
./0_setup_prereqs.sh
```
Exit the terminal and come back in.

## Run

Run the following. After step 2, verify the url the application is running on and modify `selenium_loadgen.py` with that URL.

```
./1_agent_install.sh
./2_app_install.sh
./3_app_loadgen.sh
```

## Stop/Remove

```
./99_remove_all.sh
```