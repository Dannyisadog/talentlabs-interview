from datetime import datetime, timedelta

import jwt
from ninja import Router
from ninja.security import HttpBearer

router = Router(
    tags=["Authentication"]
)

# Secret key for JWT - in production, use a secure key from settings
JWT_SECRET = "your-secret-key-here"

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            # Verify the token
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            return payload
        except:
            return None

@router.post("/fake-login", response={200: dict})
def fake_login(request):
    # Create a token that expires in 24 hours
    expiration = datetime.utcnow() + timedelta(hours=24)
    
    # Create a simple token with minimal claims
    payload = {
        "id": 1,  # Fake user ID
        "exp": expiration,
        "type": "access"
    }
    
    # Generate the token
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    
    return {
        "access_token": token,
        "token_type": "Bearer"
    } 