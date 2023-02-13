import boto3

from lambda_saleor_app.config import SECRET_PREFIX

# While running on AWS Lambda, credentials are present via IAM Role

ssm = boto3.client("ssm")


def get_from_ssm(key: str, prefix=SECRET_PREFIX) -> str:
    key_with_prefix = f"/{prefix}/{key}"
    parameter = ssm.get_parameter(Name=key_with_prefix, WithDecryption=True)
    return parameter["Parameter"]["Value"]


def write_to_ssm(key: str, value: str, prefix=SECRET_PREFIX):
    key_with_prefix = f"/{prefix}/{key}"

    ssm.put_parameter(
        Name=key_with_prefix, Value=value, Type="SecureString", Overwrite=True
    )
