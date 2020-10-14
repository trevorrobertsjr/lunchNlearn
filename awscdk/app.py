#!/usr/bin/env python3

from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ecr_assets as ecr_assets
import aws_cdk.aws_elasticloadbalancingv2 as elbv2

app = core.App()
stack = core.Stack(app, "lunchNlearn-cdk-ecs")

# Create a VPC
vpc = ec2.Vpc(stack, "lunchNlearn-cdk-vpc", max_azs=3, cidr="12.0.0.0/16")

# Create an ECS cluster
cluster = ecs.Cluster(stack, "Cluster",
    vpc=vpc
)

# Add capacity to it
cluster.add_capacity("DefaultAutoScalingGroupCapacity",
    instance_type=ec2.InstanceType("t3.xlarge"),
    desired_capacity=3
)

task_definition = ecs.Ec2TaskDefinition(stack, "TaskDef", network_mode=ecs.NetworkMode.AWS_VPC)

docker_image_asset = ecr_assets.DockerImageAsset(stack, "container-image", directory="docker")

container=task_definition.add_container("nginx-container",
    image=ecs.ContainerImage.from_docker_image_asset(docker_image_asset),
    memory_limit_mib=512
)

port_mapping = ecs.PortMapping(
    container_port=80
)

container.add_port_mappings(port_mapping)

security_group = ec2.SecurityGroup(
    stack, "nginx--web",
    vpc=vpc,
    allow_all_outbound=False
)

security_group.add_ingress_rule(
    ec2.Peer.any_ipv4(),
    ec2.Port.tcp(80)
)

# Instantiate an Amazon ECS Service
ecs_service = ecs.Ec2Service(stack, "Service",
    cluster=cluster,
    task_definition=task_definition,
    security_group=security_group,
    desired_count=3
)

lb = elbv2.ApplicationLoadBalancer(stack, "LB", vpc=vpc, internet_facing=True)
listener = lb.add_listener("Listener", port=80)
target_group1 = listener.add_targets("ecs-targets",
    port=80,
    targets=[ecs_service]
)

app.synth()