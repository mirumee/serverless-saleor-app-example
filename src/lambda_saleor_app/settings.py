from typing import Optional, Tuple, Any
from base64 import b64decode

import os

from pydantic import BaseSettings, validator
from pydantic.env_settings import SettingsSourceCallable

import boto3


class EncryptedEnv:

    def __init__(self, kms_client, key_arn: str, context: dict[str, str]):
        self.kms_client = kms_client
        self.key_arn = key_arn
        self.context = context

    def decrypt(self, encrypted: str):
        return self.kms_client.decrypt(
            CiphertextBlob=b64decode(encrypted),
            EncryptionContext=self.context,
            KeyId=self.key_arn,
        )['Plaintext'].decode('utf-8')


    def __call__(self, settings: BaseSettings) -> dict[str, Any]:
        keys = settings.schema()['properties'].keys()
        decrypted = dict()
        for key, value in ((key.lower(), value) for key,value in os.environ.items()):
            if key in keys and value.startswith('KMS:'):
                decrypted[key] = self.decrypt(value.split(':')[1])
        return decrypted


class Settings(BaseSettings):
    """
    Container for runtime configuration of the application.
    """

    debug: bool = False
    app_id: str
    saleor_domain: str
    ssm_timeout: float = 0.5

    ssm_secret_prefix: str
    kms_key_arn: str
    # AWS lambda extension env vars
    parameters_secrets_extension_http_port: int = 2773

    some_secret_text: str

    ssm_saleor_jwks_key: str = "saleor_jwks"
    ssm_saleor_app_auth_token_key: str = "saleor_app_auth_token"

    # Optional - for localstack / local development
    ssm_endpoint: Optional[str]
    # AWS boto3 env vars
    aws_access_key: Optional[str]
    aws_access_key_id: Optional[str]
    aws_secret_access_key: Optional[str]
    aws_session_token: Optional[str]
    aws_region: Optional[str]
    aws_lambda_function_name: Optional[str]
    aws_lambda_function_memory_size: Optional[str]
    aws_lambda_function_version: Optional[str]
    aws_lambda_initialization_type: Optional[str]
    aws_lambda_log_group_name: Optional[str]
    aws_lambda_log_stream_name: Optional[str]

    @validator("ssm_secret_prefix", always=True)
    def set_ssm_secret_prefix(cls, value, values):
        if value:
            return value
        return f"/{values['app_id']}"

    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return (
                init_settings,
                EncryptedEnv(
                    kms_client=boto3.client('kms'),
                    context={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']},
                    key_arn=os.environ['KMS_KEY_ARN'],
                    ),
                env_settings,
            )


settings = Settings(
    app_id="demo.lambda.app",
)
