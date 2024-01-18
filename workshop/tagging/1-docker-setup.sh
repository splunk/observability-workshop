#!/bin/bash

# This setup script will:
# (1) Fix sudo for k3s
# (2) Install docker
#
# NOTE: You will need to log out of the shell and come back in
#       after this step

# (1) Fix sudo for k3s
# NOTE: This is not generally recommended; doing this for
#       simplicity of the environment
sudo chmod +r /etc/rancher/k3s/k3s.yaml

# (2) Install docker
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo groupadd docker
sudo usermod -aG docker $USER
# Have user come back in
echo ""
echo ""
echo ""
echo Docker install complete.
echo
echo IMPORTANT NOTE: Exit out of this shell and then come back in.