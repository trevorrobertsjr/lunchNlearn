import json
import pytest

from aws_cdk import core
from awscdk.awscdk_stack import AwscdkStack


def get_template():
    app = core.App()
    AwscdkStack(app, "awscdk")
    return json.dumps(app.synth().get_stack("awscdk").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
