from typing import Optional

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """
    Container for runtime configuration of the application.
    """

    debug: bool = False
    app_id: str
    saleor_domain: str
    ssm_timeout: float = 0.5

    ssm_secret_prefix: str
    # AWS lambda extension env vars
    parameters_secrets_extension_http_port: int = 2773

    ssm_saleor_jwks_key: str = "saleor_jwks"
    ssm_saleor_app_auth_token_key: str = "saleor_app_auth_token"

    # Optional - for localstack / local development
    ssm_endpoint: Optional[str]
    # AWS boto3 env vars
    aws_access_key_id: Optional[str]
    aws_secret_access_key: Optional[str]
    aws_session_token: Optional[str]
    aws_region: Optional[str]

    @validator("ssm_secret_prefix", always=True)
    def set_ssm_secret_prefix(cls, value, values):
        if value:
            return value
        return f"/{values['app_id']}"


settings = Settings(
    app_id="demo.lambda.app",
)
