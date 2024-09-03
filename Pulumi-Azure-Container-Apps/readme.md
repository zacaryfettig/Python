
# Pulumi Azure Container Apps Deployment

## Resources created in Template
* Container App: Serverless Kubernetes instance that is controlled by Microsoft. Deploys and runs the containers.

* Load Balancer: Load Balances traffice between hosts. Used in this instance to give an entry point to the internet that can be easily locked down and secured.

* Public IP: Public IP for the Load Balancer.

* VNET: Networking Configuration.

* Load Balancer: Load Balance traffic between ECS Instances.

* Container Storage Pool: Pool of resources for the container storage to pull from.

* Container Storage: Storage Volume that will be mounted to the containers.

* Log Analytics Workspace: Resource monitoring for Container Apps

## Resource Deployment

As of 9/3/2024 Container Pools are not in GA Status. To enable preview of the feature run the command below

```
az feature  register --name "ContainerStoragePreviewAccess" --namespace Microsoft.ContainerStorage
```

Refresh provider after enabling preview

```
az provider register --name "ContainerStoragePreviewAcces" --namespace Microsoft.ContainerStorage
```

View Approval of enabling feature preview

```
az feature show --name "ContainerStoragePreviewAccess" --namespace Microsoft.ContainerStorage
```

Deploy code

```
pulumi up
```
