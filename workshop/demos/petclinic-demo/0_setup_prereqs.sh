# Install k3s
# Uses a hack to fix permission issues, should not use in production
curl -sfL https://get.k3s.io | sh -
echo "export KUBECONFIG=/etc/rancher/k3s/k3s.yaml" >> ~/.bashrc
sudo chmod +r /etc/rancher/k3s/k3s.yaml

# Install helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Setup Python
sudo apt install -y python3 python3.12-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Exit the terminal and come back in."