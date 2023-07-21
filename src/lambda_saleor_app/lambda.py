# ACHTUNG !!!
# This file is used only as a AWS lambda entry point.

import boto3

from mangum import Mangum
from fastapi import FastAPI

from lambda_saleor_app import logs
from lambda_saleor_app.settings import settings
from lambda_saleor_app.app import router
from aws_secrets_cache import Secrets
from structlog.contextvars import bind_contextvars

from aws_lambda_typing import (
    context, )

secrets = None


def setup(ctx: context.Context):
    bind_contextvars(
        aws_request_id=ctx.aws_request_id,
        function_name=ctx.function_name,
        function_arn=ctx.invoked_function_arn,
    )
    global secrets
    if not secrets:
        secrets = Secrets(
            client=boto3.client("secretsmanager"),
            prefix=settings.secret_prefix,
        )
    log = logs.setup(settings.log_level)
    return settings, log


def handler(event, ctx: context.Context):
    settings, log = setup(ctx)
    log.debug("starting handling event", lambda_event=event)
    app = FastAPI(debug=settings.debug)
    app.state.secrets = secrets
    app.include_router(router)
    hndl = Mangum(app)
    return hndl(event=event, context=ctx)
