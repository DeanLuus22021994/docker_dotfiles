"""
Security middleware for FastAPI application.

This module provides comprehensive security middleware including:
- Rate limiting
- Authentication
- CORS
- Security headers
- Input validation
"""

import time
from collections import defaultdict
from typing import Any, Awaitable, Callable, Dict, List

from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ..config.config import get_security_config
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ..config.config import get_security_config


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware using in-memory storage."""

    def __init__(self, app: Any):
        super().__init__(app)
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.config = get_security_config()

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """Process request with rate limiting."""
        if not self.config.enable_rate_limiting:
            return await call_next(request)

        # Use client IP as identifier (in production, use more sophisticated method)
        client_ip = self._get_client_ip(request)

        # Clean old requests
        current_time = time.time()
        window_start = current_time - self.config.rate_limit_window_seconds
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > window_start
        ]

        # Check rate limit
        if len(self.requests[client_ip]) >= self.config.rate_limit_requests:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "retry_after": self.config.rate_limit_window_seconds
                },
                headers={"Retry-After": str(self.config.rate_limit_window_seconds)}
            )

        # Add current request
        self.requests[client_ip].append(current_time)

        # Process request
        response = await call_next(request)
        return response

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request."""
        # Check X-Forwarded-For header first (for proxies/load balancers)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take the first IP if multiple are present
            return forwarded_for.split(",")[0].strip()

        # Fall back to X-Real-IP
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fall back to client host
        return request.client.host if request.client else "unknown"


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """API key authentication middleware."""

    def __init__(self, app: Any):
        super().__init__(app)
        self.config = get_security_config()

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """Process request with authentication."""
        if not self.config.enable_authentication:
            return await call_next(request)

        # Skip authentication for health check
        if request.url.path == "/health":
            return await call_next(request)

        # Check API key
        api_key = request.headers.get(self.config.api_key_header)
        if not api_key:
            return JSONResponse(
                status_code=401,
                content={"error": "API key required"},
                headers={"WWW-Authenticate": f"{self.config.api_key_header}"}
            )

        if api_key not in self.config.api_keys:
            return JSONResponse(
                status_code=403,
                content={"error": "Invalid API key"}
            )

        # Add API key to request state for logging
        request.state.api_key = api_key[:8] + "..."  # Log partial key only

        return await call_next(request)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Security headers middleware."""

    def __init__(self, app: Any):
        super().__init__(app)
        self.config = get_security_config()

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """Add security headers to response."""
        response = await call_next(request)

        if not self.config.enable_security_headers:
            return response

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        # HSTS (HTTP Strict Transport Security)
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = f"max-age={self.config.hsts_max_age}; includeSubDomains"

        # Content Security Policy
        if self.config.content_security_policy:
            response.headers["Content-Security-Policy"] = self.config.content_security_policy

        return response


def create_cors_middleware(app: Any) -> CORSMiddleware:
    """Create CORS middleware with configuration."""
    config = get_security_config()

    if not config.enable_cors:
        return app

    return CORSMiddleware(
        app=app,
        allow_origins=config.cors_origins,
        allow_credentials=True,
        allow_methods=config.cors_methods,
        allow_headers=config.cors_headers,
    )


def setup_security_middleware(app: Any) -> None:
    """Setup all security middleware for the FastAPI application."""
    config = get_security_config()

    # Add CORS middleware first
    if config.enable_cors:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=config.cors_origins,
            allow_credentials=True,
            allow_methods=config.cors_methods,
            allow_headers=config.cors_headers,
        )

    # Add security headers middleware
    if config.enable_security_headers:
        app.add_middleware(SecurityHeadersMiddleware)

    # Add rate limiting middleware
    if config.enable_rate_limiting:
        app.add_middleware(RateLimitMiddleware)

    # Add authentication middleware
    if config.enable_authentication:
        app.add_middleware(AuthenticationMiddleware)