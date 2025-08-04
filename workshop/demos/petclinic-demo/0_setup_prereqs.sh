sudo apt update

# Install k3s
curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE="644" sh -

# Install helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Setup Python
sudo apt install -y python3 python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f -y
google-chrome --version

# Remind to exit and come back in
echo ""
echo ""
echo "Exit the terminal and come back in."