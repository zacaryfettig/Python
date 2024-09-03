"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import resources
from pulumi_azure_native import operationalinsights
from pulumi_azure_native import resources
from pulumi_azure_native import app
import pulumi_azure_native as azure_native
import pulumi_docker as docker

resource_group = resources.ResourceGroup("rg1")
subid1 = "cb746d33-61f2-4005-a6e1-323245542be4"

# vnet
containerVnet = azure_native.network.VirtualNetwork("virtualNetwork",
    address_space={
        "address_prefixes": ["10.0.0.0/16"],
    },
    location="westus2",
    resource_group_name=resource_group.name,
    subnets=[{
        "address_prefix": "10.0.0.0/24",
        "name": "subnet1",
    }],
    virtual_network_name="containerVnet")

workspace = operationalinsights.Workspace("loganalytics",
    resource_group_name=resource_group.name,
    sku=operationalinsights.WorkspaceSkuArgs(name="PerGB2018"),
    retention_in_days=30)

workspace_shared_keys = pulumi.Output.all(resource_group.name, workspace.name) \
    .apply(lambda args: operationalinsights.get_shared_keys(
        resource_group_name=args[0],
        workspace_name=args[1]
    ))


#pool = azure_native.containerstorage.Pool("pool",
#    assignments=[{
#        "id": "$self/container_app",
#    }],
#    location="eastus2",
#    pool_name="pool1",
#    pool_type={
#        "ephemeral_disk": {
#            "replicas": 3,
#        },
#    },
#    reclaim_policy=azure_native.containerstorage.ReclaimPolicy.DELETE,
#    resource_group_name=resource_group.name,
#    resources={
#        "requests": {
#            "storage": 30000,
#        },
#    },
#    tags={
#        "key1888": "value1888",
#    },
#    zones=[
#        azure_native.containerstorage.Zone.ZONE1,
#        azure_native.containerstorage.Zone.ZONE2,
#        azure_native.containerstorage.Zone.ZONE3,
#    ])

#volume = azure_native.containerstorage.Volume("containerVol",
#    capacity_gi_b=25838,
#    labels={
#        "key2039": "value2039",
#    },
#    pool_name=pool.name,
#    resource_group_name=resource_group.name,
#    volume_name="wordpress")

managed_env = app.ManagedEnvironment("env",
    resource_group_name=resource_group.name,
    app_logs_configuration=app.AppLogsConfigurationArgs(
        destination="log-analytics",
        log_analytics_configuration=app.LogAnalyticsConfigurationArgs(
            customer_id=workspace.customer_id,
            shared_key=workspace_shared_keys.apply(lambda r: r.primary_shared_key)
    )))

container_app = app.ContainerApp("app",
    resource_group_name=resource_group.name,
    managed_environment_id=managed_env.id,
    configuration=app.ConfigurationArgs(
        ingress=app.IngressArgs(
            external=False,
            target_port=80
        ),
    ),
    template=app.TemplateArgs(
        containers = [
            app.ContainerArgs(
                name="wordpress",
                image="docker.io/wordpress",
                ),
            app.VolumeMountArgs(
                mount_path="/var/www/html",
                volume_name="fileshare",
            ),
#            app.VolumeArgs(
#                storage_type="AzureFile",
#            ),
        ])
        )

public_ip_address = azure_native.network.PublicIPAddress("publicIPAddress",
    location="westus2",
    public_ip_address_name="lbIP",
    resource_group_name=resource_group.name,
     sku={
        "name": "Standard",
        "tier": "Regional",
     },
     public_ip_allocation_method=azure_native.network.IPAllocationMethod.STATIC,
        )

load_balancer = azure_native.network.LoadBalancer("loadBalancer",
    backend_address_pools=[{
        "name": "be-lb",
        "ip_address": container_app.outbound_ip_addresses[0],
        "virtual_network": {
        "id": containerVnet.id,
    },
    }],
    frontend_ip_configurations=[{
        "name": "fe-lb",
        "linkedPublicIPAddress": public_ip_address.ip_address,
        "public_ip_address": {
#            "ip_address": public_ip_address.ip_address
            "id": public_ip_address.id
        },
                }],
    sku={
        "name": azure_native.network.LoadBalancerSkuName.STANDARD,
    },
    probes=[{
        "interval_in_seconds": 15,
        "name": "probe-lb",
        "number_of_probes": 2,
        "port": 80,
        "probe_threshold": 1,
        "protocol": azure_native.network.ProbeProtocol.HTTP,
        "request_path": "healthcheck.aspx",
    }],
    load_balancer_name="lb",
   load_balancing_rules=[{
        "backend_address_pool": {
            "id": "$self/backendAddressPools/be-lb",
        },
        "frontend_port": 80,
        "backend_port": 80,
        "enable_floating_ip": True,
        "frontend_ip_configuration": {
            "id": "$self/frontendIPConfigurations/fe-lb"
        },
        "idle_timeout_in_minutes": 15,
        "load_distribution": azure_native.network.LoadDistribution.DEFAULT,
        "name": "rulelb",
       "probe": {
            "id": "$self/probes/probe-lb", #"/subscriptions/cb746d33-61f2-4005-a6e1-323245542be4/resourceGroups/rg11c62dedf/providers/Microsoft.Network/loadBalancers/loadBalancer73270bb8/probes/probe-lb",
        },
        "protocol": azure_native.network.TransportProtocol.TCP,
    }],
    resource_group_name=resource_group.name)