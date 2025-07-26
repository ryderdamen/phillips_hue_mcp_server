import os
import logging
from typing import Dict, Any, Optional, Callable
from functools import wraps
from authentication import verify_google_token_from_headers

logger = logging.getLogger(__name__)

# Global context for storing current request info
_request_context = {}

def set_request_context(headers: Dict[str, str]):
    """Set the current request context for authentication."""
    global _request_context
    _request_context = headers

def get_request_context() -> Dict[str, str]:
    """Get the current request context."""
    global _request_context
    return _request_context

def require_auth(func: Callable) -> Callable:
    """Simple decorator to require Google OAuth authentication."""
    @wraps(func)
    def wrapper(**kwargs):
        try:
            # Get headers from the global context
            headers = get_request_context()
            
            if headers and 'Authorization' in headers:
                # Verify the token
                user = verify_google_token_from_headers(headers)
                logger.info(f"Authenticated user: {user.get('email')}")
                # Authentication successful, just call the function
                return func(**kwargs)
            else:
                # For development, allow access without auth
                logger.warning("No authentication headers found, allowing access for development")
                return func(**kwargs)
                
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return {"error": "Authentication required", "details": str(e)}
    
    return wrapper

def create_oauth_metadata():
    """Create OAuth metadata for client configuration."""
    return {
        "issuer": "https://accounts.google.com",
        "authorization_server": "https://accounts.google.com",
        "resource": os.environ.get('TAILSCALE_FUNNEL_URL', 'http://localhost:8000'),
        "scopes": {
            "openid": "Basic identity",
            "email": "User email"
        }
    } 