import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_ec2_sacale_set+ebs.cdk_ec2_sacale_set+ebs_stack import CdkEc2SacaleSet+ebsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_ec2_sacale_set+ebs/cdk_ec2_sacale_set+ebs_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkEc2SacaleSet+ebsStack(app, "cdk-ec2-sacale-set-ebs")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
