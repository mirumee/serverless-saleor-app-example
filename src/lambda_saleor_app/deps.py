from fastapi import Request, Depends, Header
from saleor_sdk.crypto.utils import decode_webook_payload, decode_jwt
from saleor_sdk.crypto.exceptions import JWKSKeyMissing

from lambda_saleor_app.utils.jwks import get_jwkset


async def get_host(request: Request):
    # Fetches host from API Gateway
    try:
        return request.scope["aws.event"]["requestContext"]["domainName"]
    except KeyError:
        # Fallback to Host header
        return request.headers["host"]


async def get_saleor_event(saleor_event: str = Header(..., alias="Saleor-Event")):
    return saleor_event


async def get_saleor_domain(saleor_domain: str = Header(..., alias="Saleor-Domain")):
    # TODO: these will always be single tenant apps, we should make them sticky to only one Salor instance
    # and validate here if the incoming domain is the one configured in settings.
    return saleor_domain


async def get_saleor_signature(
    saleor_signature: str = Header(..., alias="Saleor-Signature")
):
    return saleor_signature


async def get_saleor_user(
    saleor_domain: str = Depends(get_saleor_domain),
    saleor_token: str = Header(..., alias="Saleor-Token"),
):
    saleor_jwks = await get_jwkset()
    max_attempts = 1

    # TODO: fix DRY with verify_webhook_signature
    while max_attempts:
        try:
            return decode_jwt(
                jwt=saleor_token,
                jwks=saleor_jwks,
            )
        except JWKSKeyMissing as exc:
            if max_attempts:
                saleor_jwks = await get_jwkset()
                max_attempts -= 1
            else:
                raise


async def verify_webhook_signature(
    request: Request,
    saleor_domain: str = Depends(get_saleor_domain),
    jws: str = Depends(get_saleor_signature),
):
    saleor_jwks = await get_jwkset()

    max_attempts = 1

    while max_attempts:
        try:
            return decode_webook_payload(
                jws=jws,
                jwks=saleor_jwks,
                webhook_payload=await request.body(),
            )
        except JWKSKeyMissing as exc:
            if max_attempts:
                saleor_jwks = await get_jwkset()
                max_attempts -= 1
            else:
                raise
