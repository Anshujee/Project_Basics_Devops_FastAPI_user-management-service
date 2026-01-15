First we verify that EKS is up and running . 
After that we check all context using command - 
kubectl config get-contexts   

After that we move to the active current context by using command - 
kubectl config current-context

then we have to run command to connect with the eks clustor using coomand 
aws eks update-kubeconfig \
  --region us-west-2 \
  --name <your-cluster-name> # here in my case cluster name is my-eks-cluster

  so full command is 
  aws eks update-kubeconfig \
  --region us-west-2 \
  --name my-eks-cluster

  After then we move inside the k8s folder of our project and run the deplyment.yml and services .ymal fie using command 

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
This command will create pods and services for our app . 
to check pods are running or not we have to run command 
kubectl get pods
Expected Output is - 
nshujee@Anshus-MacBook-Air k8s % kubectl get pods 
NAME                              READY   STATUS    RESTARTS   AGE
ums-deployment-7cdc688b47-4lk2m   1/1     Running   0          9m26s
ums-deployment-7cdc688b47-dpk6b   1/1     Running   0          9m26s

similarlly to check deplyment are running we use command - 
kubectl get deployments
Expected output is - 
kubectl get deployments
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
ums-deployment   2/2     2            2           11m

Same for services - 
kubectl get services

Expected output is -

kubectl get services
NAME          TYPE           CLUSTER-IP       EXTERNAL-IP                                                             PORT(S)        AGE
kubernetes    ClusterIP      172.20.0.1       <none>                                                                  443/TCP        42m
ums-service   LoadBalancer   172.20.253.132   a718a0d6e3d0d4ef4977e5e25f05bc94-89937777.us-west-2.elb.amazonaws.com   80:31975/TCP   12m

Now we can access the application using amazon provided url " http://a718a0d6e3d0d4ef4977e5e25f05bc94-89937777.us-west-2.elb.amazonaws.com/health"

kubectl get all -- to get all resources in kubernetes .

Now run command ---  kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
to delete all the resources in kubernetes. 


