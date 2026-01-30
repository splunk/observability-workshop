# 1. Install the apache2-utils package, which provides the htpasswd command

sudo apt install apache2-utils

# 2. Create an HTPasswd file with participant credentials
htpasswd -c -B -b users.htpasswd participant1 TempPass123!

for i in {2..30}; do
  htpasswd -B -b users.htpasswd participant$i TempPass123!
done

# 3. Replace the ROSA-managed HTPasswd IdP with a custom one
rosa delete idp -c $CLUSTER_NAME cluster-admin
rosa create idp -c $CLUSTER_NAME --type htpasswd --name workshop-users --from-file users.htpasswd
