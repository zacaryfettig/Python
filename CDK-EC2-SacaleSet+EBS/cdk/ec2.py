from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_cloudwatch as cloudwatch,
)
from constructs import Construct

class ec2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc1 = ec2.Vpc(
            self,
            "VPC1",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="subnet1",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                )
            ],
        )

        keyPair = ec2.CfnKeyPair(
            self,
            "ec2KeyPair",
            key_name="cdk-ec2-key-pair",
        )

        sg = ec2.SecurityGroup(
            self, "MySecurityGroup", vpc=vpc1, allow_all_outbound=True
        )

        sg.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow SSH access"
        )

        auto_scaling_group = autoscaling.AutoScalingGroup(self, "AutoScalingEc2",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc1,
            security_group=sg,
            associate_public_ip_address=True,
            key_name=keyPair.key_name,
            block_devices=[autoscaling.BlockDevice(
                device_name="/dev/sdf",
                volume=autoscaling.BlockDeviceVolume.ebs(15,
                    volume_type=autoscaling.EbsDeviceVolumeType.GP2
                )
            )
            ]
        )

        worker_utilization_metric = cloudwatch.Metric(
            namespace="MyService",
            metric_name="WorkerUtilization"
)

        auto_scaling_group.scale_on_metric("ScaleToCPU",
            metric=worker_utilization_metric,
            scaling_steps=[autoscaling.ScalingInterval(upper=10, change=-1), autoscaling.ScalingInterval(lower=70, change=+1), autoscaling.ScalingInterval(lower=85, change=+2)
            ],
            evaluation_periods=10,
            datapoints_to_alarm=5,
            adjustment_type=autoscaling.AdjustmentType.CHANGE_IN_CAPACITY
)