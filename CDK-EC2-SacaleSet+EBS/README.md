# EC2 Instance in a ScaleSet with EBS Persistent Storage

## Resources created in Template
* EC2 Instance: AWS Compute

* VPC: Networking Configuration

* Autoscaling: Adds and Removes ec2 instances based on capacity

* Cloud Watch: Monitors resource statistics and is used by Autoscaling to determine when to scale up/down

* Secuirty Group: Allows/Denys network traffic based on rules

## Autoscaling setup
Autoscaling is set to Step Scaling. It will add 1 instance when CPU is 70% or over. It will add two instances when cpu is 85%. When CPU is at 10% it will remove 1.

## Resource Deployment

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

Deploy code

```
$ cdk deploy
```
