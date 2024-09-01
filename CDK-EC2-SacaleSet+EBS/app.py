#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.ec2 import ec2Stack


app = cdk.App()
ec2Stack(app, "ec2")

app.synth()
