# EC2 Instance in a ScaleSet with EBS Persistent Storage

## Resources created in Template
* EC2 Instance: AWS Compute

* VPC: Networking Configuration

* Autoscaling: Adds and Removes ec2 instances based on capacity

* Cloud Watch: Monitors resource statistics and is used by Autoscaling to determine when to scale up/down

* Secuirty Group: Allows/Denys network traffic based on rules

## Resource Deployment

```
terraform init
```

```
terraform plan
```

```
terraform apply
```

#### Deployment Terms
terraform init: Run terraform init to initialize the Terraform deployment. This command downloads the Azure modules required to manage your Azure resources.

terraform plan: creates an execution plan, but doesn't execute it. Instead, it determines what actions are necessary to create the configuration specified in your configuration files.

terraform apply: apply the execution plan to your cloud infrastructure.


















# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
