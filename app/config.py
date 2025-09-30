from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./savannah_orders.db"
    TEST_DATABASE_URL: Optional[str] = "sqlite:///./test_savannah_orders.db"

    # Security
    SECRET_KEY: str = "your-secret-key-for-development-only-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # OpenID Connect
    OIDC_ISSUER: str = "https://dev-example.auth0.com/"
    OIDC_CLIENT_ID: str = "example-client-id"
    OIDC_CLIENT_SECRET: str = "example-client-secret"

    # Africa's Talking
    AT_USERNAME: str = "sandbox"  # Sandbox environment username
    AT_API_KEY: str = ("atsk_6ddd843b21bb370dc50942b7d887d67e8e7c346c46121ba3573b3a8c7a76bfae9d8f6372")  # noqa: E501
    AT_SENDER_ID: str = ""  # Use SAVANNAH as sender ID

    # Application
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
