# Grant each user access to their namespace only
for i in {1..20}; do
  oc adm policy add-role-to-user admin participant$i -n workshop-participant-$i
done
