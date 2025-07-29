# Setup Python
cd /home/ubuntu
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt 

# Add the python loadgen to systemd
sudo cp ./petclinic_owners_loadgen.service /etc/systemd/system