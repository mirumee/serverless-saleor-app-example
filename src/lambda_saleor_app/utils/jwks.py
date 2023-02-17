import httpx
from jwt.api_jwk import PyJWKSet

from lambda_saleor_app.settings import settings
from lambda_saleor_app.utils import parameter_store


async def fetch_jwks(saleor_domain: str = settings.saleor_domain):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://{saleor_domain}/.well-known/jwks.json")
        return response.content.decode()


async def refresh_jwks():
    raw_jwks = await fetch_jwks(saleor_domain=settings.saleor_domain)
    parameter_store.write_to_ssm(settings.ssm_saleor_jwks_key, raw_jwks)
    return raw_jwks


async def get_jwkset() -> PyJWKSet:
    raw_jwks = parameter_store.get_from_ssm(settings.ssm_saleor_jwks_key)
    if not raw_jwks:
        raw_jwks = await refresh_jwks()
    return PyJWKSet.from_json(raw_jwks)
