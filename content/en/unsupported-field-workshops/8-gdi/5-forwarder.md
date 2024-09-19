---
title: Monitor System Logs with Splunk Universal Forwarder
linkTitle: 5. UF Deployment
weight: 5
---

**Objective:** Learn how to monitor Linux system logs with the Universal Forwarder sending logs to Splunk Enterprise

**Duration**: 10 Minutes

## Scenario

You've been tasked with monitoring the OS logs of the host running your Kubernetes cluster. We are going to utilize a script that will autodeploy the Splunk Universal Forwarder. You will then configure the Universal Forwarder to send logs to the Splunk Enterprise instance assigned to you.

### 1. Ensure You're in the Correct Directory

- we will need to be in /home/splunk/session-2

``` bash
cd /home/splunk/session-2
```

### 2. Review the Universal Forwarder Install Script

- Let's take a look at the script that will install the Universal Forwarder and Linux TA automatically for you.
  - This script is primarily used for remote instances.
  - Note we are not using a deployment server in this lab, however it is recommended in production we do that.
  - What user are we installing Splunk as?

``` bash
#!/bin/sh  
# This EXAMPLE script shows how to deploy the Splunk universal forwarder
# to many remote hosts via ssh and common Unix commands.
# For "real" use, this script needs ERROR DETECTION AND LOGGING!!
# --Variables that you must set -----
# Set username using by splunkd to run.
  SPLUNK_RUN_USER="ubuntu"

# Populate this file with a list of hosts that this script should install to,
# with one host per line. This must be specified in the form that should
# be used for the ssh login, ie. username@host
#
# Example file contents:
# splunkuser@10.20.13.4
# splunkker@10.20.13.5
  HOSTS_FILE="myhost.txt"

# This should be a WGET command that was *carefully* copied from splunk.com!!
# Sign into splunk.com and go to the download page, then look for the wget
# link near the top of the page (once you have selected your platform)
# copy and paste your wget command between the ""
  WGET_CMD="wget -O splunkforwarder-9.0.3-dd0128b1f8cd-Linux-x86_64.tgz 'https://download.splunk.com/products/universalforwarder/releases/9.0.3/linux/splunkforwarder-9.0.3-dd0128b1f8cd-Linux-x86_64.tgz'"
# Set the install file name to the name of the file that wget downloads
# (the second argument to wget)
  INSTALL_FILE="splunkforwarder-9.0.3-dd0128b1f8cd-Linux-x86_64.tgz"

# After installation, the forwarder will become a deployment client of this
# host.  Specify the host and management (not web) port of the deployment server
# that will be managing these forwarder instances.
# Example 1.2.3.4:8089
#  DEPLOY_SERVER="x.x.x.x:8089"



# After installation, the forwarder can have additional TA's added to the 
# /app directory please provide the local where TA's will be. 
  TA_INSTALL_DIRECTORY="/home/splunk/session-2"

# Set the seed app folder name for deploymentclien.conf
#  DEPLOY_APP_FOLDER_NAME="seed_all_deploymentclient"
# Set the new Splunk admin password
  PASSWORD="buttercup"

REMOTE_SCRIPT_DEPLOY="
  cd /opt
  sudo $WGET_CMD
  sudo tar xvzf $INSTALL_FILE
  sudo rm $INSTALL_FILE
  #sudo useradd $SPLUNK_RUN_USER
  sudo find $TA_INSTALL_DIRECTORY -name '*.tgz' -exec tar xzvf {} --directory /opt/splunkforwarder/etc/apps \;
  sudo chown -R $SPLUNK_RUN_USER:$SPLUNK_RUN_USER /opt/splunkforwarder
  echo \"[user_info] 
  USERNAME = admin
  PASSWORD = $PASSWORD\" > /opt/splunkforwarder/etc/system/local/user-seed.conf   
  #sudo cp $TA_INSTALL_DIRECTORY/*.tgz /opt/splunkforwader/etc/apps/
  #sudo find /opt/splunkforwarder/etc/apps/ -name '*.tgz' -exec tar xzvf {} \;
  #sudo -u splunk /opt/splunkforwarder/bin/splunk start --accept-license --answer-yes --auto-ports --no-prompt
  /opt/splunkforwarder/bin/splunk start --accept-license --answer-yes --auto-ports --no-prompt
  #sudo /opt/splunkforwarder/bin/splunk enable boot-start -user $SPLUNK_RUN_USER
  /opt/splunkforwarder/bin/splunk enable boot-start -user $SPLUNK_RUN_USER
  #sudo cp $TA_INSTALL_DIRECTORY/*.tgz /opt/splunkforwarder/etc/apps/

  exit
 "

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"


#===============================================================================================
  echo "In 5 seconds, will run the following script on each remote host:"
  echo
  echo "===================="
  echo "$REMOTE_SCRIPT_DEPLOY"
  echo "===================="
  echo 
  sleep 5
  echo "Reading host logins from $HOSTS_FILE"
  echo
  echo "Starting."
  for DST in `cat "$DIR/$HOSTS_FILE"`; do
    if [ -z "$DST" ]; then
      continue;
    fi
    echo "---------------------------"
    echo "Installing to $DST"
    echo "Initial UF deployment"
    sudo ssh -t "$DST" "$REMOTE_SCRIPT_DEPLOY"
  done  
  echo "---------------------------"
  echo "Done"
  echo "Please use the following app folder name to override deploymentclient.conf options: $DEPLOY_APP_FOLDER_NAME"
```
  
### 3. Run the install script

We will run the install script now. You will see some Warnings at the end. This is totally normal. The script is built for use on remote machines, however for todays lab you will be using localhost.

``` bash
./install.sh
```

You will be asked `Are you sure you want to continue connecting (yes/no/[fingerprint])?`
Answer Yes.

Enter your ssh password when prompted.

### 4. Verify installation of the Universal Forwarader

- We need to verify that the Splunk Universal Forwarder is installed and running.
  - You should see a couple PID's return and a "Splunk is currently running." message.

``` bash
/opt/splunkforwarder/bin/splunk status
```

#### 5. Configure the Universal Forwarder to Send Data to Splunk Enterprise

- We will be able to send the data to our Splunk Enterprise environment easily by entering one line into the cli.
  - [Universal Forwarder Config Guide](https://docs.splunk.com/Documentation/Forwarder/9.0.3/Forwarder/Configuretheuniversalforwarder)

``` bash
/opt/splunkforwarder/bin/splunk add forward-server <your_splunk_enterprise_ip>:9997
```

#### 6. Verify the Data in Your Splunk Enterprise Environment

- We are now going to take a look at the Splunk Enterprise environment to verify logs are coming in.
  - Logs will be coming into ```index=main```

- Open your web browser and navigate to: ```http://<your_splunk_enterprise_ip:8000```
  - You will use the credentials ```admin:<your_ssh_password>```

- In the search bar, type in the following:
- ```index=main host=<your_host_name>```

- You should see data from your host. Take note of the interesting fields and the different data sources flowing in.
