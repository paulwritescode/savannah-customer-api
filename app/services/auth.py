from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from jose.exceptions import JWTClaimsError, ExpiredSignatureError
from datetime import datetime, timedelta
import httpx
import json
from typing import Dict, Any, Optional
from app.config import settings

security = HTTPBearer()

class AuthService:
    def __init__(self):
        self.issuer = settings.OIDC_ISSUER
        self.client_id = settings.OIDC_CLIENT_ID
        self.jwks_uri = f"{self.issuer}.well-known/jwks.json"
        self._jwks_cache = None
        self._jwks_cache_time = None
    
    async def get_jwks(self) -> Dict[str, Any]:
        """Fetch and cache JWKS from OpenID Connect issuer"""
        if self._jwks_cache and self._jwks_cache_time and \
           (datetime.utcnow() - self._jwks_cache_time).seconds < 3600:  # Cache for 1 hour
            return self._jwks_cache
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.jwks_uri)
                response.raise_for_status()
                self._jwks_cache = response.json()
                self._jwks_cache_time = datetime.utcnow()
                return self._jwks_cache
        except Exception as e:
            # Fallback to local verification for demo purposes
            return None
    
    async def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        """
        Verify JWT token according to OpenID Connect standards
        """
        try:
            # For demo purposes, we'll use local verification
            # In production, you would use the JWKS from the issuer
            payload = jwt.decode(
                credentials.credentials,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
                options={
                    "verify_signature": True,
                    "verify_aud": False,  # Skip audience verification for demo
                    "verify_iss": False,  # Skip issuer verification for demo
                    "verify_exp": True,
                    "verify_nbf": True,
                    "verify_iat": True
                }
            )
            
            # Validate required OpenID Connect claims
            if not self._validate_oidc_claims(payload):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token claims"
                )
            
            return {
                "sub": payload.get("sub"),
                "username": payload.get("sub"),
                "scopes": payload.get("scopes", []),
                "iss": payload.get("iss"),
                "aud": payload.get("aud"),
                "exp": payload.get("exp"),
                "iat": payload.get("iat")
            }
            
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except JWTClaimsError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token claims: {str(e)}"
            )
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}"
            )
    
    def _validate_oidc_claims(self, payload: Dict[str, Any]) -> bool:
        """Validate OpenID Connect required claims"""
        required_claims = ["sub", "iss", "aud", "exp", "iat"]
        
        for claim in required_claims:
            if claim not in payload:
                return False
        
        # Validate audience (should match client_id)
        aud = payload.get("aud")
        if isinstance(aud, list):
            if self.client_id not in aud:
                return False
        elif aud != self.client_id:
            return False
        
        # Validate issuer
        iss = payload.get("iss")
        if iss != self.issuer:
            return False
        
        return True
    
    def create_access_token(self, data: dict):
        """
        Create JWT token with OpenID Connect standard claims
        """
        now = datetime.utcnow()
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # OpenID Connect standard claims
        to_encode = {
            "iss": self.issuer,  # Issuer
            "aud": self.client_id,  # Audience
            "sub": data.get("sub", "user"),  # Subject
            "iat": now,  # Issued at
            "exp": expire,  # Expiration
            "nbf": now,  # Not before
            "scopes": data.get("scopes", []),  # Custom scopes
            "username": data.get("sub", "user"),  # Custom username
        }
        
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def require_scope(self, required_scope: str):
        def scope_checker(user_info = Depends(self.verify_token)):
            user_scopes = user_info.get("scopes", [])
            if required_scope not in user_scopes and "admin" not in user_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            return user_info
        return scope_checker

auth_service = AuthService()
