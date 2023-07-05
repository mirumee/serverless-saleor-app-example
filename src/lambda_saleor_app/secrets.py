import boto3
from aws_secrets_cache import Secrets

secrets = Secrets(client=boto3.client("secretsmanager"))
