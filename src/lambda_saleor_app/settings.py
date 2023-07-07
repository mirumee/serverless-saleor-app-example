from typing import Optional

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """
    Container for runtime configuration of the application.
    """

    log_level: str = "info"
    debug: bool = False
    app_id: str
    saleor_domain: str

    secret_prefix: str = None

    saleor_jwks_key: str = "saleor_jwks"
    saleor_app_auth_token_key: str = "saleor_app_auth_token"

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

    @validator("secret_prefix", always=True)
    def set_secret_prefix(cls, value, values):
        if value:
            return value
        return f"/{values['app_id']}/"

    @validator("log_level")
    def level_to_py(cls, value: str):
        value = value.upper()
        if value not in ("INFO", "ERROR", "DEBUG", "CRITICAL"):
            raise ValueError(f"Invalid log level {value!r}")
        return value


settings = Settings(app_id="demo.lambda.app")
