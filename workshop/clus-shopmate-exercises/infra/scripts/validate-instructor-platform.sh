#!/usr/bin/env bash
set -euo pipefail

echo "== Kubernetes nodes =="
kubectl get nodes -o wide

echo
echo "== GPU Operator pods =="
kubectl get pods -n gpu-operator -o wide

echo
echo "== DCGM services =="
kubectl get svc -A | grep -i dcgm || {
  echo "No DCGM service found yet." >&2
  exit 1
}

echo
echo "== NIM pods =="
kubectl get pods -A | grep -i nim || {
  echo "No NIM pod found yet. Deploy NIM before final event validation." >&2
  exit 1
}

echo
echo "== Student namespace sample =="
kubectl get namespace student-01
kubectl auth can-i create deployments --as=system:serviceaccount:student-01:student -n student-01

echo
echo "== Shared student kubeconfig access =="
for ns in $(seq -f 'student-%02g' 1 20); do
  kubectl auth can-i create pods/portforward \
    --as=system:serviceaccount:workshop-access:workshop-students \
    -n "$ns" | grep -qx yes
  kubectl auth can-i get endpoints \
    --as=system:serviceaccount:workshop-access:workshop-students \
    -n "$ns" | grep -qx yes
  kubectl auth can-i list endpointslices.discovery.k8s.io \
    --as=system:serviceaccount:workshop-access:workshop-students \
    -n "$ns" | grep -qx yes
done
