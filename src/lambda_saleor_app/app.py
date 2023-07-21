import structlog

from fastapi import Request, Depends, APIRouter

from lambda_saleor_app.settings import settings
from lambda_saleor_app.schemas import InstallAuthToken
from lambda_saleor_app.deps import get_host, verify_webhook_signature

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.get("/manifest.json")
async def manifest(request_host: str = Depends(get_host)):
    """
    Endpoint used to establish permissions and webhook subscriptions
    """
    return {
        "id": settings.app_id,
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


@router.post("/register")
async def register(request: Request, auth_token: InstallAuthToken):
    """
    Endpoint that handles final step of App installation - persisting the Saleor Token
    """
    logger.info("Persisting Saleor Token")
    request.app.state.secrets[
        settings.saleor_app_auth_token_key
    ] = auth_token.auth_token
    return "OK"


@router.post("/api/webhooks/order-event")
async def webhook(request: Request, __=Depends(verify_webhook_signature)):
    """
    Public endpoint for receiving a webhook from Saleor
    """
    payload = await request.json()
    logger.debug("Webhook request", body=payload, headers=request.headers)
    return payload


@router.get("/app")
async def dashboard_app(request: Request):
    """
    This endpoint is responsible for displaying the dashboard view of embedded app
    """
    return {
        "message": "Hello from Lambda",
        "saleor_domain": request.query_params.get("domain"),
        "saleor_api_url": request.query_params.get("SaleorApiUrl"),
        "stored_token": request.app.state.secrets[settings.saleor_app_auth_token_key],
    }
