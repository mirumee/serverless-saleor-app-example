from fastapi import FastAPI, Request
from mangum import Mangum

from lambda_saleor_app import config
from lambda_saleor_app.utils import logging, parameter_store

logger = logging.logger


app = FastAPI(debug=True)


@app.get("/manifest.json")
async def manifest(request: Request):
    """
    Endpoint used to establish permissions and webhook subscriptions
    """
    # Fetches host from API Gateway
    try:
        request_host = request.scope["aws.event"]["requestContext"]["domainName"]
    except KeyError:
        # Fallback to Host header
        request_host = request.headers["host"]

    return {
        "id": config.APP_ID,
        "version": "1.0.0",
        "name": "My serverless App",
        "about": "My serverless App for extending Saleor.",
        "permissions": ["MANAGE_ORDERS"],
        "appUrl": f"https://{request_host}/app",
        "tokenTargetUrl": f"https://{request_host}/register",
        "dataPrivacy": "Lorem ipsum",
        "dataPrivacyUrl": f"https://{request_host}/app/data-privacy",
        "homepageUrl": f"https://{request_host}/homepage",
        "supportUrl": f"https://{request_host}/support",
        "extensions": [],
        "webhooks": [
            {
                "name": "Multiple order's events",
                "asyncEvents": ["ORDER_CREATED", "ORDER_UPDATED"],
                "query": "subscription { event { ... on OrderCreated { order { id }} ... on OrderUpdated { order { id, created, user {email, firstName} }}}}",
                "targetUrl": f"https://{request_host}/api/webhooks/order-event",
                "isActive": True,
            }
        ],
    }


@app.post("/register")
async def register(request: Request):
    """
    Endpoint that handles final step of App installation - persisting the Saleor Token
    """
    body = await request.json()
    logger.debug("Register request", body=body)
    auth_token = body.get("auth_token")
    if auth_token:
        logger.info("Persisting Saleor Token")
        parameter_store.write_to_ssm(key="SaleorAPIKey", value=auth_token)
    return "OK"


@app.post("/api/webhooks/order-event")
async def webhook(request: Request):
    """
    Public endpoint for receiving a webhook from Saleor
    """
    payload = await request.json()
    logger.info("Webhook request", body=payload, headers=request.headers)
    # TODO: Verify webhook signature using Saleor-Domain and Saleor-Signature headers
    return payload


@app.get("/app")
async def dashboard_app(request: Request):
    """
    This endpoint is responsible for displaying the dashboard view of embedded app
    """
    return {
        "message": "Hello from Lambda",
        "saleor_domain": request.query_params.get("domain"),
        "saleor_api_url": request.query_params.get("SaleorApiUrl"),
        "stored_token": parameter_store.get_from_ssm(
            "SaleorAPIKey"
        ),  # FIXME: Demo only, insecure
    }


handler = Mangum(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, log_level="info")
