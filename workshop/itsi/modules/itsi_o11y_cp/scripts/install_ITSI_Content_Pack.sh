#! /bin/bash
# Version 2.0

PASSWORD=$1
VERSION=$2
FILENAME=$3
LICENSE_FILE=$4
APP_FOR_CONTENT_PACKS_FILE=$5
IT_SERVICE_INTELLIGENCE_FILE=$6
SYNTHETIC_MONITORING_ADD_ON_FILE=$7 
INFRASTRUCTURE_MONITORING_ADD_ON_FILE=$8
INPUTS_DOT_CONF="inputs.conf"

sudo apt update
# download packages from s3 bucket
wget -O /tmp/$APP_FOR_CONTENT_PACKS_FILE "https://o11yitsicpbuckettestisma.s3.eu-west-1.amazonaws.com/$APP_FOR_CONTENT_PACKS_FILE" --append-output=logfile
wget -O /tmp/$IT_SERVICE_INTELLIGENCE_FILE "https://o11yitsicpbuckettestisma.s3.eu-west-1.amazonaws.com/$IT_SERVICE_INTELLIGENCE_FILE" --append-output=logfile
wget -O /tmp/$SYNTHETIC_MONITORING_ADD_ON_FILE "https://o11yitsicpbuckettestisma.s3.eu-west-1.amazonaws.com/$SYNTHETIC_MONITORING_ADD_ON_FILE" --append-output=logfile
wget -O /tmp/$INFRASTRUCTURE_MONITORING_ADD_ON_FILE "https://o11yitsicpbuckettestisma.s3.eu-west-1.amazonaws.com/$INFRASTRUCTURE_MONITORING_ADD_ON_FILE" --append-output=logfile
wget -O /tmp/$INPUTS_DOT_CONF "https://o11yitsicpbuckettestisma.s3.eu-west-1.amazonaws.com/$INPUTS_DOT_CONF" --append-output=logfile

# download and install splunk
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
tar -xvf /tmp/$IT_SERVICE_INTELLIGENCE_FILE -C /opt/splunk/etc/apps
tar -xvf /tmp/$INFRASTRUCTURE_MONITORING_ADD_ON_FILE -C /opt/splunk/etc/apps
tar -xvf /tmp/$SYNTHETIC_MONITORING_ADD_ON_FILE -C /opt/splunk/etc/apps
tar -xvf /tmp/$APP_FOR_CONTENT_PACKS_FILE -C /opt/splunk/etc/apps

# ensure rights are given for the content pack
sudo chown splunk:splunk -R /opt/splunk/etc/apps

# ensure inputs.conf reflects in the UI
sudo chmod 755 -R /opt/splunk/etc/apps/itsi/local

# start splunk
/opt/splunk/bin/splunk start

# install ITSI NFR license
curl -k -u admin:$PASSWORD https://localhost:8089/services/licenser/licenses -d "name=/tmp/$LICENSE_FILE"
/opt/splunk/bin/splunk restart

# Add Modular Input
sudo cat /tmp/inputs.conf >> /opt/splunk/etc/apps/itsi/local/inputs.conf

# ensure rights are applied to all folders
sudo chown splunk:splunk -R /opt/splunk/etc/apps

# restart splunk
/opt/splunk/bin/splunk restart