# Install k3s
curl -sfL https://get.k3s.io | sh - 

# Install helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Setup Python
sudo apt install -y python3 python3.12-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt