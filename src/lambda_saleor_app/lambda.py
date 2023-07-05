from mangum import Mangum

from lambda_saleor_app import logs
from lambda_saleor_app.settings import settings
from lambda_saleor_app.app import app
from structlog.contextvars import bind_contextvars

from aws_lambda_typing import (
    context,
)


def setup(ctx: context.Context):
    bind_contextvars(
        aws_request_id=ctx.aws_request_id,
        function_name=ctx.function_name,
        function_arn=ctx.invoked_function_arn,
    )
    log = logs.setup(settings.log_level)
    return settings, log


def handler(event, ctx: context.Context):
    settings, log = setup(ctx)
    log.debug("lambda event", lambda_event=event)
    handler = Mangum(app)
    handler(event=event, context=ctx)
