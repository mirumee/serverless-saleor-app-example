import urllib.parse
from urllib.error import URLError
import json
import boto3
from botocore.client import Config

from lambda_saleor_app.settings import settings

# While running on AWS Lambda, credentials are present via IAM Role
ssm = boto3.client(
    "ssm",
    config=Config(connect_timeout=settings.ssm_timeout, read_timeout=settings.ssm_timeout),
    endpoint_url=settings.ssm_endpoint,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region,
)


def param_store_cache(key: str, prefix=settings.ssm_secret_prefix) -> str:
    """
    Retrieve parameters from AWS Parameter store.
    In order for this to work on lambda read docs below.
    https://docs.aws.amazon.com/systems-manager/latest/userguide/ps-integration-lambda-extensions.html
    """
    params = urllib.parse.urlencode({
        'name': f"{prefix}/{key}",
        'withDecryption': True,
    })
    port = settings.parameters_secrets_extension_http_port
    req = urllib.request.Request(f'http://localhost:{port}/systemsmanager/parameters/get?{params}')
    req.add_header('X-Aws-Parameters-Secrets-Token', settings.aws_session_token)
    try:
        response = json.loads(urllib.request.urlopen(req).read().decode())
        return response['Parameter']['Value']
    except URLError:
        return ""


def get_from_ssm(key: str, prefix=settings.ssm_secret_prefix) -> str:
    value = param_store_cache(key, prefix)
    if value:
        return value
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
