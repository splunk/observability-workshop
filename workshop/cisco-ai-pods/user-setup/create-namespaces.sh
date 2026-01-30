# Create namespaces
for i in {1..30}; do
  kubectl create namespace workshop-participant-$i
done

# Apply resource quotas to each namespace
kubectl apply -f resource-quota.yaml -n workshop-participant-$i