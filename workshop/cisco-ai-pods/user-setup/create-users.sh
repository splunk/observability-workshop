# 1. Create an HTPasswd file with participant credentials

htpasswd -c -B -b users.htpasswd participant1 TempPass123!

for i in {2..20}; do
  htpasswd -B -b users.htpasswd participant$i TempPass123!
done

# ... repeat for all participants

# 2. Create the HTPasswd secret in OpenShift
oc create secret generic htpass-secret \
  --from-file=htpasswd=users.htpasswd \
  -n openshift-config

# 3. Configure the HTPasswd identity provider
oc apply -f - <<EOF
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
  name: cluster
spec:
  identityProviders:
  - name: workshop-users
    mappingMethod: claim
    type: HTPasswd
    htpasswd:
      fileData:
        name: htpass-secret
EOF

# 4. Grant each user access to their namespace only
for i in {1..20}; do
  oc adm policy add-role-to-user admin participant$i -n workshop-participant-$i
done
