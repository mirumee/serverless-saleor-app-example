import httpx
from jwt.api_jwk import PyJWKSet

from lambda_saleor_app.settings import settings
from aws_secrets_cache import Secrets


async def fetch_jwks(saleor_domain: str = settings.saleor_domain):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://{saleor_domain}/.well-known/jwks.json")
        return response.content.decode()


async def refresh_jwks(secrets: Secrets):
    raw_jwks = await fetch_jwks(saleor_domain=settings.saleor_domain)
    secrets[settings.saleor_jwks_key] = raw_jwks
    return raw_jwks


async def get_jwkset(secrets: Secrets) -> PyJWKSet:
    raw_jwks = secrets[settings.saleor_jwks_key]
    if not raw_jwks:
        raw_jwks = await refresh_jwks(secrets)
    return PyJWKSet.from_json(raw_jwks)
