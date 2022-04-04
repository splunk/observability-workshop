#! /bin/bash
# Version 2.0

PASSWORD=$1
VERSION=$2
FILENAME=$3
LICENSE_FILE=$6

wget -O /tmp/$FILENAME "https://download.splunk.com/products/splunk/releases/$VERSION/linux/$FILENAME"
sudo dpkg -i /tmp/$FILENAME
sudo /opt/splunk/bin/splunk start --accept-license --answer-yes --no-prompt --seed-passwd $PASSWORD
sudo /opt/splunk/bin/splunk enable boot-start

# install java
sudo apt install -y default-jre
JAVA_HOME=$(realpath /usr/bin/java)

# stop splunk
sudo /opt/splunk/bin/splunk stop

# install apps
tar -xvf /tmp/splunk-it-service-intelligence_4113.spl -C /opt/splunk/etc/apps
tar -xvf /tmp/splunk-infrastructure-monitoring-add-on_121.tgz -C /opt/splunk/etc/apps
tar -xvf /tmp/splunk-synthetic-monitoring-add-on_107.tgz -C /opt/splunk/etc/apps
tar -xvf /tmp/splunk-app-for-content-packs_140.spl -C /opt/splunk/etc/apps

# ensure rights are given for the content pack
sudo chown splunk:splunk -R /opt/splunk/etc/apps

# ensure inputs.conf reflects in the UI
sudo chmod 755 -R /opt/splunk/etc/apps/itsi/local

# start splunk
/opt/splunk/bin/splunk start

# install ITSI NFR license
curl -k -u admin:$PASSWORD https://localhost:8089/services/licenser/licenses -d "name=$LICENSE_FILE"
sudo /opt/splunk/bin/splunk restart


# Add Modular Input
sudo cat /tmp/inputs.conf >> /opt/splunk/etc/apps/itsi/local/inputs.conf

# restart splunk
/opt/splunk/bin/splunk restart