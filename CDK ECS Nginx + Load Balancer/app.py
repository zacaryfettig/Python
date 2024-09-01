#!/usr/bin/env python3

import aws_cdk as cdk
#from cdk.cdk_ECS import ECSCluster
#from cdk.cdk_ECS import ECSService
#from cdk.cdk_ECS import 
from cdk.cdk_ECS import ecsStack

app = cdk.App()
ecsStack(app, "ecs-stack")

app.synth()
