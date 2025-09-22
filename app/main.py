from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import customers, orders
from app.database import engine
from app.models import customer, order
from app.config import settings
from app.services.auth import auth_service

# Create database tables
customer.Base.metadata.create_all(bind=engine)
order.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Savannah Orders API",
    description="Customer and Order Management System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(customers.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Savannah Orders API v1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# OpenID Connect Discovery Endpoints
@app.get("/.well-known/openid_configuration")
async def openid_configuration():
    """OpenID Connect Discovery endpoint"""
    return {
        "issuer": settings.OIDC_ISSUER,
        "authorization_endpoint": f"{settings.OIDC_ISSUER}authorize",
        "token_endpoint": f"{settings.OIDC_ISSUER}oauth/token",
        "userinfo_endpoint": f"{settings.OIDC_ISSUER}userinfo",
        "jwks_uri": f"{settings.OIDC_ISSUER}.well-known/jwks.json",
        "response_types_supported": ["code", "id_token", "token"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": ["RS256", "HS256"],
        "scopes_supported": ["openid", "profile", "email", "read", "write"],
        "token_endpoint_auth_methods_supported": ["client_secret_post", "client_secret_basic"]
    }

@app.get("/.well-known/jwks.json")
async def jwks():
    """JSON Web Key Set endpoint"""
    return {
        "keys": [
            {
                "kty": "oct",
                "use": "sig",
                "kid": "savannah-key-1",
                "alg": "HS256"
            }
        ]
    }

# Token endpoint for demo purposes
@app.post("/oauth/token")
async def token_endpoint():
    """OAuth2/OIDC token endpoint for demo"""
    # In a real implementation, this would handle authorization code flow
    # For demo purposes, we'll return a pre-generated token
    token_data = {
        "sub": "demo-user",
        "scopes": ["read", "write"]
    }
    access_token = auth_service.create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "scope": "read write"
    }
