Deploy with `gcloud container clusters create dwk-cluster --zone=europe-west1-b --cluster-version=1.32 --disk-size=32 --num-nodes=3 --machine-type=e2-small && gcloud container clusters get-credentials dwk-cluster --zone=europe-west1-b && kubectl apply -f manifests/namespace.yaml && sleep 5 && kubectl apply -f manifests/config.yaml && kubectl apply -f manifests/service.yaml && kubectl apply -f manifests/deployment.yaml && kubectl apply -f manifests/ingress.yaml`

Get the ingress address with `kubectl get ing`
