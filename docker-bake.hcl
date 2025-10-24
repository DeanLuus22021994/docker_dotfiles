# Comprehensive Docker Bake configuration for all stacks and services
# Generated: 2025-10-25
# Enables Docker Buildx and Bake features for optimized container builds across all stacks

variable "REGISTRY" {
  default = ""
}

variable "TAG" {
  default = "latest"
}

variable "BUILDKIT_INLINE_CACHE" {
  default = "1"
}

variable "DOCKER_BUILDKIT" {
  default = "1"
}

# Global cache configuration
variable "LOCAL_CACHE_DIR" {
  default = ".cache/buildx"
}

variable "REGISTRY_CACHE_PREFIX" {
  default = "${REGISTRY}cache-"
}

variable "ENABLE_REGISTRY_CACHE" {
  default = "false"
}

# Base target with common configuration
target "base" {
  dockerfile = ".devcontainer/devcontainer.dockerfile"
  context = "."
  platforms = ["linux/amd64"]
  args = {
    BUILDKIT_INLINE_CACHE = "${BUILDKIT_INLINE_CACHE}"
  }
  cache-from = [
    "type=local,src=${LOCAL_CACHE_DIR}",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}devcontainer-${TAG}" : ""}"
  ]
  cache-to = [
    "type=local,dest=${LOCAL_CACHE_DIR},mode=max",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}devcontainer-${TAG},mode=max" : ""}"
  ]
  output = ["type=docker"]
}

# Devcontainer targets
target "devcontainer-dev" {
  inherits = ["base"]
  tags = [
    "${REGISTRY}devcontainer:dev-${TAG}",
    "${REGISTRY}devcontainer:latest"
  ]
  target = "base"
  secret = [
    "id=github_token,env=GITHUB_TOKEN"
  ]
  cache-from = [
    "type=local,src=${LOCAL_CACHE_DIR}",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}devcontainer-${TAG}" : ""}"
  ]
  cache-to = [
    "type=local,dest=${LOCAL_CACHE_DIR},mode=max",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}devcontainer-${TAG},mode=max" : ""}"
  ]
}

target "devcontainer-prod" {
  inherits = ["base"]
  tags = [
    "${REGISTRY}devcontainer:prod-${TAG}"
  ]
  args = {
    BUILDKIT_INLINE_CACHE = "${BUILDKIT_INLINE_CACHE}"
    PRODUCTION_BUILD = "true"
  }
  cache-from = [
    "type=local,src=${LOCAL_CACHE_DIR}",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}devcontainer-prod-${TAG}" : ""}"
  ]
  cache-to = [
    "type=local,dest=${LOCAL_CACHE_DIR},mode=max",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}devcontainer-prod-${TAG},mode=max" : ""}"
  ]
}

target "devcontainer-ci" {
  inherits = ["devcontainer-dev"]
  tags = [
    "${REGISTRY}devcontainer:ci-${TAG}"
  ]
  cache-from = [
    "type=gha,scope=devcontainer-${TAG}",
    "type=registry,ref=${REGISTRY_CACHE_PREFIX}devcontainer-${TAG}"
  ]
  cache-to = [
    "type=gha,scope=devcontainer-${TAG},mode=max",
    "type=registry,ref=${REGISTRY_CACHE_PREFIX}devcontainer-${TAG},mode=max"
  ]
  attest = [
    "type=provenance,mode=max",
    "type=sbom"
  ]
}

# Python service targets for different environments
target "python-dev" {
  dockerfile = ".dockerfiles/python.Dockerfile"
  context = "."
  platforms = ["linux/amd64"]
  tags = [
    "${REGISTRY}python:dev-${TAG}",
    "${REGISTRY}docker_python:latest"
  ]
  args = {
    ENVIRONMENT = "development"
    SERVICE_TYPE = "app"
    WORKERS = "1"
  }
  cache-from = [
    "type=local,src=${LOCAL_CACHE_DIR}",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}python-dev-${TAG}" : ""}"
  ]
  cache-to = [
    "type=local,dest=${LOCAL_CACHE_DIR},mode=max",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}python-dev-${TAG},mode=max" : ""}"
  ]
  target = "app"
}

target "python-prod" {
  inherits = ["python-dev"]
  tags = [
    "${REGISTRY}python:prod-${TAG}"
  ]
  args = {
    ENVIRONMENT = "production"
    SERVICE_TYPE = "app"
    WORKERS = "4"
  }
  cache-from = [
    "type=local,src=${LOCAL_CACHE_DIR}",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}python-prod-${TAG}" : ""}"
  ]
  cache-to = [
    "type=local,dest=${LOCAL_CACHE_DIR},mode=max",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}python-prod-${TAG},mode=max" : ""}"
  ]
}

target "python-test" {
  inherits = ["python-dev"]
  tags = [
    "${REGISTRY}python:test-${TAG}"
  ]
  args = {
    ENVIRONMENT = "test"
    SERVICE_TYPE = "app"
    WORKERS = "1"
  }
  cache-from = [
    "type=local,src=${LOCAL_CACHE_DIR}",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}python-test-${TAG}" : ""}"
  ]
  cache-to = [
    "type=local,dest=${LOCAL_CACHE_DIR},mode=max",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}python-test-${TAG},mode=max" : ""}"
  ]
}

target "python-mcp" {
  inherits = ["python-dev"]
  tags = [
    "${REGISTRY}python:mcp-${TAG}"
  ]
  args = {
    ENVIRONMENT = "test"
    SERVICE_TYPE = "mcp"
    WORKERS = "1"
  }
  cache-from = [
    "type=local,src=${LOCAL_CACHE_DIR}",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}python-mcp-${TAG}" : ""}"
  ]
  cache-to = [
    "type=local,dest=${LOCAL_CACHE_DIR},mode=max",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}python-mcp-${TAG},mode=max" : ""}"
  ]
}

# Node.js service targets
target "node-dev" {
  dockerfile = ".dockerfiles/node.Dockerfile"
  context = "."
  platforms = ["linux/amd64"]
  tags = [
    "${REGISTRY}node:dev-${TAG}",
    "${REGISTRY}docker_node:latest"
  ]
  args = {
    ENVIRONMENT = "development"
  }
  cache-from = [
    "type=local,src=${LOCAL_CACHE_DIR}",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}node-dev-${TAG}" : ""}"
  ]
  cache-to = [
    "type=local,dest=${LOCAL_CACHE_DIR},mode=max",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}node-dev-${TAG},mode=max" : ""}"
  ]
  target = "app"
}

target "node-prod" {
  inherits = ["node-dev"]
  tags = [
    "${REGISTRY}node:prod-${TAG}"
  ]
  args = {
    ENVIRONMENT = "production"
  }
  cache-from = [
    "type=local,src=${LOCAL_CACHE_DIR}",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}node-prod-${TAG}" : ""}"
  ]
  cache-to = [
    "type=local,dest=${LOCAL_CACHE_DIR},mode=max",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}node-prod-${TAG},mode=max" : ""}"
  ]
}

# GitHub Actions Runner target
target "runner" {
  dockerfile = ".compose/github-actions-runner/Dockerfile"
  context = ".compose/github-actions-runner"
  platforms = ["linux/amd64"]
  tags = [
    "${REGISTRY}runner:${TAG}",
    "${REGISTRY}docker_runner:latest"
  ]
  cache-from = [
    "type=local,src=${LOCAL_CACHE_DIR}",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}runner-${TAG}" : ""}"
  ]
  cache-to = [
    "type=local,dest=${LOCAL_CACHE_DIR},mode=max",
    "${ENABLE_REGISTRY_CACHE == "true" ? "type=registry,ref=${REGISTRY_CACHE_PREFIX}runner-${TAG},mode=max" : ""}"
  ]
}

# Stack-specific groups
group "basic-stack" {
  targets = ["python-dev", "node-dev"]
}

group "cluster-stack" {
  targets = ["python-prod", "node-prod"]
}

group "mcp-stack" {
  targets = ["python-mcp"]
}

group "swarm-stack" {
  targets = ["python-prod", "node-prod"]
}

group "ci-stack" {
  targets = ["devcontainer-ci", "python-test", "node-dev", "runner"]
}

# All services group
group "all-services" {
  targets = ["devcontainer-dev", "devcontainer-prod", "python-dev", "python-prod", "python-test", "python-mcp", "node-dev", "node-prod", "runner"]
}

# Default target
target "default" {
  inherits = ["devcontainer-dev"]
}
