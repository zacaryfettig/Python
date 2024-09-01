from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_iam as iam,
)


class ecsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        execution_role1 = iam.Role(self, "ecs-devops-execution-role", assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"), role_name="ecs-devops-execution-role")

        execution_role1.add_to_policy(iam.PolicyStatement( effect=iam.Effect.ALLOW, resources=["*"], actions=["ecr:GetAuthorizationToken", "ecr:BatchCheckLayerAvailability", "ecr:GetDownloadUrlForLayer", "ecr:BatchGetImage", "logs:CreateLogStream", "logs:PutLogEvents"] ))

# vpc: ec2.Vpc
        vpcEcs = ec2.Vpc(self, "vpcEcs")

# Create an ECS cluster
        cluster = ecs.Cluster(self, "Cluster", vpc=vpcEcs)

# Add capacity to it
        cluster.add_capacity("DefaultAutoScalingGroupCapacity",
            instance_type=ec2.InstanceType("t2.large"),
           desired_capacity=2
        )

        task_definition = ecs.Ec2TaskDefinition(self, "TaskDef", execution_role=execution_role1)

        task_definition.add_container("ecsContainer",
           image=ecs.ContainerImage.from_registry("docker.io/nginx"),
           memory_limit_mib=4000,
           port_mappings=[ecs.PortMapping(container_port=80)], 
        )
        # Instantiate an Amazon ECS Service
        service = ecs.Ec2Service(self, "Service",
            cluster=cluster,
            task_definition=task_definition
        )

        lb = elbv2.ApplicationLoadBalancer(self, "LB", vpc=vpcEcs, internet_facing=True)
        listener = lb.add_listener("Listener", port=80)
        target_group1 = listener.add_targets("ECS1",
            port=80,
            targets=[service.load_balancer_target(
        container_name="ecsContainer",
        container_port=80
    )]
            )
        
        