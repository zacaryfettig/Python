"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources
from pulumi_azure_native import containerregistry
from pulumi_azure_native import operationalinsights
from pulumi_azure_native import resources
from pulumi_azure_native import app
import pulumi_docker as docker

resource_group = resources.ResourceGroup("rg1")

workspace = operationalinsights.Workspace("loganalytics",
    resource_group_name=resource_group.name,
    sku=operationalinsights.WorkspaceSkuArgs(name="PerGB2018"),
    retention_in_days=30)

workspace_shared_keys = pulumi.Output.all(resource_group.name, workspace.name) \
    .apply(lambda args: operationalinsights.get_shared_keys(
        resource_group_name=args[0],
        workspace_name=args[1]
    ))

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
            external=True,
            target_port=80
        ),
    ),
    template=app.TemplateArgs(
        containers = [
            app.ContainerArgs(
                name="nginx",
                image="docker.io/nginx")
        ]))