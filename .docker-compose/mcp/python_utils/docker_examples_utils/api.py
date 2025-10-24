#!/usr/bin/env python3
"""
FastAPI web server for Docker Examples Python utilities.

Provides REST API endpoints for documentation utilities,
leveraging Python 3.14 features for enhanced performance.

This module implements a FastAPI web server that exposes various
documentation utilities as REST endpoints. It includes correlation ID
tracking, structured logging, and leverages Python 3.14+ features
for improved performance.

Endpoints:
    GET /: API information and available endpoints
    GET /health: Health check with system status
    GET /inventory: Component inventory generation
    GET /links/check: Link validation service

Features:
    - Correlation ID tracking for request tracing
    - Structured JSON logging
    - Python 3.14+ feature detection and utilization
    - Comprehensive error handling
    - Async endpoint support
"""

import datetime
import json
import sys
import threading
import uuid
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.responses import JSONResponse

from .config.config import LogLevel
from .config.settings import (
    HTTPConfig,
    LoggingConfig,
    PathConfig,
    get_python_features,
)
from .core.security import setup_security_middleware
from .models.models import InventoryRequest, LinkCheckRequest

path_config = PathConfig()
http_config = HTTPConfig()
features = get_python_features()

logging_config = LoggingConfig(level=LogLevel.INFO)
logging_config.configure_logging()

app = FastAPI(
    title="Docker Examples Python Utilities API",
    description="FastAPI web server for Docker Examples Python utilities",
    version="0.2.0",
)

# Setup security middleware
setup_security_middleware(app)

status_lock = threading.Lock()
init_status: dict[str, Any] = {
    "status": "initializing",
    "timestamp": datetime.datetime.now().isoformat(),
    "services": {},
}


@app.middleware("http")
async def add_correlation_id(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    Middleware to add correlation ID tracking to all requests.

    This middleware ensures every request has a correlation ID for
    distributed tracing and logging. If no correlation ID is provided
    in the request headers, a new UUID is generated.

    Args:
        request: FastAPI request object
        call_next: Next middleware/endpoint in the chain

    Returns:
        Response: Modified response with correlation ID header
    """
    try:
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id

        return response
    except Exception:
        # Fallback error response if middleware fails
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "correlation_id": str(uuid.uuid4())},
        )


@app.get("/")
async def root(request: Request) -> dict[str, Any]:
    """
    Root endpoint providing API information.

    Returns basic API information including version, Python features,
    and available endpoints.

    Args:
        request: FastAPI request object

    Returns:
        dict: API information and available endpoints
    """
    correlation_logger = logging_config.get_correlation_logger(
        request.state.correlation_id
    )
    correlation_logger.info("Root endpoint accessed", extra={"endpoint": "/"})

    return {
        "message": "Docker Compose Utils Python Utilities API",
        "version": "0.2.0",
        "python_version": features["version_string"],
        "free_threaded": features["is_free_threaded"],
        "interpreters": features["has_interpreters"],
        "endpoints": {
            "/inventory": "Component inventory",
            "/health": "Health check",
            "/links/check": "Link validation",
        },
    }


@app.get("/health")
async def health(request: Request) -> JSONResponse:
    """
    Health check endpoint.

    Provides system health information including Python version,
    available features, and service status.

    Args:
        request: FastAPI request object

    Returns:
        JSONResponse: Health status information
    """
    correlation_logger = logging_config.get_correlation_logger(
        request.state.correlation_id
    )
    correlation_logger.info("Health check requested", extra={"endpoint": "/health"})

    with status_lock:
        current_status = init_status.copy()

    current_status.update({"python_version": sys.version, "features": features})

    correlation_logger.info(
        "Health check completed",
        extra={
            "status": current_status["status"],
            "response_size": len(json.dumps(current_status)),
        },
    )

    return JSONResponse(content=current_status)


@app.get("/inventory")
async def get_inventory(
    request: Request, inventory_request: InventoryRequest
) -> JSONResponse:
    """
    Generate component inventory from source files.

    Analyzes the specified source directory for React/TypeScript components
    and generates a categorized inventory.

    Args:
        request: FastAPI request object
        src_path: Source directory path (default: "src")

    Returns:
        JSONResponse: Component inventory with summary statistics

    Raises:
        HTTPException: If inventory generation fails
    """
    correlation_logger = logging_config.get_correlation_logger(
        request.state.correlation_id
    )
    correlation_logger.info(
        "Inventory generation requested",
        extra={"endpoint": "/inventory", "src_path": inventory_request.src_path},
    )

    try:
        from .models.models import ComponentInventoryConfig
        from .services.component_inventory import (
            ComponentInventoryService,
        )

        config = ComponentInventoryConfig(src_path=inventory_request.src_path)
        service = ComponentInventoryService(config, path_config)
        inventory = service.generate_inventory()

        summary = {
            "pages": len(inventory.get("pages", [])),
            "components": len(inventory.get("components", [])),
            "hooks": len(inventory.get("hooks", [])),
            "utils": len(inventory.get("utils", [])),
        }

        correlation_logger.info(
            "Inventory generation completed",
            extra={"summary": summary, "success": True},
        )

        return JSONResponse(
            content={"status": "success", "data": inventory, "summary": summary}
        )
    except Exception as e:
        correlation_logger.error(
            "Inventory generation failed",
            extra={"error": str(e), "src_path": inventory_request.src_path},
        )
        raise HTTPException(
            status_code=500, detail=f"Error generating inventory: {str(e)}"
        ) from e


@app.get("/links/check")
async def check_links(
    request: Request, link_request: LinkCheckRequest = Depends()
) -> JSONResponse:
    """
    Validate links in documentation files.

    Performs concurrent link checking on all documentation files
    using the specified number of workers and timeout.

    Args:
        request: FastAPI request object
        workers: Number of concurrent workers (default: 10)
        timeout: Request timeout in seconds (default: 10)

    Returns:
        JSONResponse: Link validation results with summary statistics

    Raises:
        HTTPException: If link checking fails
    """
    correlation_logger = logging_config.get_correlation_logger(
        request.state.correlation_id
    )
    correlation_logger.info(
        "Link checking requested",
        extra={"endpoint": "/links/check", "workers": link_request.workers, "timeout": link_request.timeout},
    )

    try:
        from .models.models import LinkCheckConfig
        from .services.link_checker import LinkCheckerService

        config = LinkCheckConfig(
            max_workers=link_request.workers,
            timeout=link_request.timeout,
            use_interpreters=features["has_interpreters"],
        )

        service = LinkCheckerService(config, path_config, http_config)
        results = service.check_links_concurrent()

        summary = {
            "valid": len(results.get("valid", [])),
            "broken": len(results.get("broken", [])),
            "skipped": len(results.get("skipped", [])),
        }

        correlation_logger.info(
            "Link checking completed", extra={"summary": summary, "success": True}
        )

        return JSONResponse(
            content={"status": "success", "data": results, "summary": summary}
        )
    except Exception as e:
        correlation_logger.error(
            "Link checking failed",
            extra={"error": str(e), "workers": link_request.workers, "timeout": link_request.timeout},
        )
        raise HTTPException(
            status_code=500, detail=f"Error checking links: {str(e)}"
        ) from e


if __name__ == "__main__":
    import uvicorn

    print("🐍 Docker Compose Utils Python Utilities API")
    print(f"📍 Python {features['version_string']}")
    if features["is_free_threaded"]:
        print("🧵 Running in free-threaded mode")
    if features["has_interpreters"]:
        print("🔄 Concurrent interpreters available")

    uvicorn.run(
        "docker_examples_utils.api:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
    )
