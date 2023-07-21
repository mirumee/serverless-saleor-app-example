from fastapi import FastAPI
import uvicorn
import logs
import boto3

from lambda_saleor_app.app import router
from settings import settings
from aws_secrets_cache import Secrets


def main():
    app = FastAPI(debug=settings.debug)
    app.include_router(router)
    app.state.secrets = Secrets(
        client=boto3.client("secretsmanager"),
        prefix=settings.secret_prefix,
    )
    # logs.setup(settings.log_level)
    uvicorn.run(
        app,
        host="localhost",
        port=8000,
        log_level=settings.log_level.lower(),
        reload=False,
    )


if __name__ == "__main__":
    main()
