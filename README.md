# kubernetes_01
## Exercises
### Chapter 2
- [1.1](https://github.com/oju-31/kubernetes_01/tree/1.1)
- [1.2](https://github.com/oju-31/kubernetes_01/tree/1.2)
- [1.3](https://github.com/oju-31/kubernetes_01/tree/1.3)

from 1.6:
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2

from 1.11
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube

from 3.1
gcloud container clusters create dwk-cluster --zone=europe-west1-b --cluster-version=1.32 --disk-size=32 --num-nodes=3 --machine-type=e2-small

gcloud container clusters delete dwk-cluster --zone=europe-west1-b

gcloud container clusters get-credentials dwk-cluster --zone=europe-west1-b

kubectl delete all,cm,secret,pvc,gateway,httproute --all

http://34.128.149.61
