---
title: GDI - Real Time Enrichment Workshop
linkTitle: Getting started
weight: 2
---

Please note to begin the following lab, you must have gone through the following:

- Download and place the yelp dataset in /var/appdata/
- Obtain a Splunk Observability Cloud access key
- [Clone this repository](https://github.com/leungsteve/realtime_enrichment)
- Access to a K8 environment (e.g. k3s on multipass) python3

Follow these steps if using O11y Workshop EC2 instances

``` bash
#note: verify yelp data files are present
ll /var/appdata/yelp*

export SPLUNK_ACCESS_TOKEN=<your access token>
export SPLUNK_REALM=<your realm>
export ACCESS_TOKEN=<your access token>
export REALM=<your realm>
export clusterName=<your-cluster>


git clone https://github.com/leungsteve/realtime_enrichment.git
cd realtime_enrichment/workshop
python3 -m venv rtapp-workshop
source rtapp-workshop/bin/activate
```

Follow these steps if you are using MULTIPASS:

``` bash
#IMPORTANT NOTE:
#run this on your mac
#run this on your multipass ubuntu VM (e.g. multipass shell <vm name>)

#1. Yelp dataset placed in /var/appdata/
#extract then move the yelp dataset (json) to /var/appdata
sudo mkdir -p /var/appdata/
sudo chmod 777 /var/appdata/
mv <yelp*json> /var/appdata/
ll /var/appdata/yelp*

*output*
-rw-r--r--@ 1 stevel  staff   124380583 Jan 28  2021 /var/appdata/yelp_academic_dataset_business.json
-rw-r--r--@ 1 stevel  staff  6936678061 Jan 28  2021 /var/appdata/yelp_academic_dataset_review.json
-rw-r--r--@ 1 stevel  staff  3684505303 Jan 28  2021 /var/appdata/yelp_academic_dataset_user.json
*output*

#3. Copy Workshop files to /var/appdata/Workshop on your Mac
cd  /var/appdata

#4. a K8 environment (e.g. k3s on multipass)
#create a multipass VM., present the yelp dataset to the VM
multipass launch --name test4cpu16gb --cpus 4 --mem 16Gb --disk 32GB
#makes the yelp dataset available to your VM
multipass mount /var/appdata test4cpu16gb
multipass shell test4cpu16gb
ubuntu@test4cpu8gb:~$ ll /var/appdata/yelp*
-rw-r--r-- 1 ubuntu ubuntu  124380583 Jan 28  2021 /var/appdata/yelp_academic_dataset_business.json
-rw-r--r-- 1 ubuntu ubuntu 6936678061 Jan 28  2021 /var/appdata/yelp_academic_dataset_review.json
-rw-r--r-- 1 ubuntu ubuntu 3684505303 Jan 28  2021 /var/appdata/yelp_academic_dataset_user.json

curl -sfL https://get.k3s.io | sh -
curl -s https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
sudo mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown `whoami`. ~/.kube/config
echo 'export KUBECONFIG=~/.kube/config' >> ~/.bashrc
source ~/.bashrc

#5. python3
#recommended to create and work in a virtual environment (on your mac. not in multipass)
python3 --version
Python 3.10.0

cd Workshop
python3 -m venv rtapp-workshop
source rtapp-workshop/bin/activate
#new prompt:
#(rtapp-workshop)  
```
