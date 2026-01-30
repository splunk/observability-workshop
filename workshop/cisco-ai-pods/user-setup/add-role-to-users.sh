# Grant each user access to their namespace only
for i in {1..30}; do
  oc adm policy add-role-to-user admin participant$i -n workshop-participant-$i
done
