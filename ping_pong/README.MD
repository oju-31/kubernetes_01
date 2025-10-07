Deploy with `gcloud container clusters create dwk-cluster --zone=europe-west1-b --cluster-version=1.32 --disk-size=32 --num-nodes=3 --machine-type=e2-small && gcloud container clusters get-credentials dwk-cluster --zone=europe-west1-b && gcloud container clusters update dwk-cluster --region=europe-west1-b --gateway-api=standard && kubectl apply -f manifests`

Get the Gateway address with `kubectl get gateway log-pong-gateway`
