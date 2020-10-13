#!/usr/bin/env python3

from aws_cdk import core

from awscdk.awscdk_stack import AwscdkStack


app = core.App()
AwscdkStack(app, "awscdk", env={'region': 'us-west-2'})

app.synth()
