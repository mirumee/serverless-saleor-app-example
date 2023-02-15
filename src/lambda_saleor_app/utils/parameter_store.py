import botocore
import boto3
from botocore.client import Config

from lambda_saleor_app.settings import settings

# While running on AWS Lambda, credentials are present via IAM Role
ssm = boto3.client(
    "ssm",
    config=Config(connect_timeout=settings.ssm_timeout, read_timeout=settings.ssm_timeout),
    endpoint_url=settings.ssm_endpoint,
    aws_access_key_id=settings.ssm_aws_access_key_id,
    aws_secret_access_key=settings.ssm_aws_secret_access_key,
    region_name=settings.ssm_region,
)


def get_from_ssm(key: str, prefix=settings.ssm_secret_prefix) -> str:
    key_with_prefix = f"{prefix}/{key}"
    try:
        parameter = ssm.get_parameter(Name=key_with_prefix, WithDecryption=True)
    except ssm.exceptions.ParameterNotFound:
        return None
    return parameter["Parameter"]["Value"]


def write_to_ssm(key: str, value: str, prefix=settings.ssm_secret_prefix):
    key_with_prefix = f"{prefix}/{key}"

    ssm.put_parameter(
        Name=key_with_prefix, Value=value, Type="SecureString", Overwrite=True
    )
