# Pet clinic demo

This demo will help demonstrate using call graphs. It introduces some latency to diagnose with that capability.

It assumes you are using a vm with a /home/ubuntu directory, which it will populate. Use at your own risk.

## Pre-requisites

To setup this demo, deploy the following on a linux host with systemd. (NOTE: You can run this without systemd with pretty basic changes if desired.)
* [k3s](https://k3s.io/)
* [helm](https://helm.sh/)
* [python](https://www.python.org/) with pip

This assumes you are cloning this repo from /home/ubuntu. If you do it in a different directory you may need to adjust some of these files.

## Preparation

```
cd /home/ubuntu
git clone https://github.com/splunk/observability-workshop.git
mv observability-workshop/workshop .
cp observability-workshop/workshop/demos/petclinic-demo/* .
rm -r observability-workshop
```

## One time Setup

```
./0_setup_prereqs.sh
```

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