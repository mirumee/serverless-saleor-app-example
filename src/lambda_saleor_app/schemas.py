from pydantic import BaseModel


class InstallAuthToken(BaseModel):
    auth_token: str
