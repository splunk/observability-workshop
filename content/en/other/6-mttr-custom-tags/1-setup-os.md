---
title: Setting up your AWS Instance
linkTitle: 1. Setup - OS
weight: 1
---

## Environment Setup - Mac

{{% notice title="Note" style="info" %}}
If you wish to run this on Mac directly, you can see the instructions [here in the appendix](./appendix-a-setup-mac) and skip the next section on Linux.

All installs must continue at [setting up the app](./2-setup-app).
{{% /notice %}}

## Environment Setup - Linux

You can skip past the EC2 configuration to Linux Software Requirements if you already have an Ec2 that meets the specifications below !!!!

* ubuntu 22.04

![1-setup-config-1](../images/1-setup-config-1.png)
![1-setup-config-2](../images/1-setup-config-2.png)
![1-setup-config-3](../images/1-setup-config-3.png)

* Security Group Security Settings
  * HTTP inbound open on 8010
  * All Traffic open outbound

![1-setup-config-4](../images/1-setup-config-4.png)

* Linux Software Requirements: docker, docker-compose, git, maven

``` bash
sudo apt update
sudo apt upgrade
sudo apt install docker docker-compose maven
```
