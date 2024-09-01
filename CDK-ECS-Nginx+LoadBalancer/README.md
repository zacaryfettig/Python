# ECS Containter Nginx Deployment

## Resources created in Template
* Cluster: Container Cluster

* Task Definition: The Task holds the container image and information that is used to deploy the containers in the cluster

* Service: Works to make sure that the tasks are running based on the specifications in the configuration

* VPC: Networking Configuration

* Load Balancer: Load Balance traffic between ECS Instances

* Execution Role: Allows ECS to talk to and be run on the EC2 Instances

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
