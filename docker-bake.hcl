# Docker Bake configuration for advanced build caching and multi-target builds
# This file enables Docker Buildx and Bake features for optimized container builds

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

# Base target with common configuration
target "base" {
  dockerfile = ".devcontainer/devcontainer.dockerfile"
  context = "."
  platforms = ["linux/amd64"]
  args = {
    BUILDKIT_INLINE_CACHE = "${BUILDKIT_INLINE_CACHE}"
  }
  cache-from = [
    "type=local,src=/tmp/.buildx-cache"
  ]
  cache-to = [
    "type=local,dest=/tmp/.buildx-cache-new,mode=max"
  ]
  # Export cache for reuse
  output = ["type=docker"]
}

# Development target with full features
target "dev" {
  inherits = ["base"]
  tags = [
    "${REGISTRY}devcontainer:dev-${TAG}",
    "${REGISTRY}devcontainer:latest"
  ]
  target = "base"
  # Enable build secrets for secure credential handling
  secret = [
    "id=github_token,env=GITHUB_TOKEN"
  ]
  # Use registry cache for faster builds
  cache-from = [
    "type=local,src=/tmp/.buildx-cache",
    "type=registry,ref=${REGISTRY}devcontainer:cache-${TAG}"
  ]
  cache-to = [
    "type=local,dest=/tmp/.buildx-cache-new,mode=max",
    "type=registry,ref=${REGISTRY}devcontainer:cache-${TAG},mode=max"
  ]
}

# Production target with minimal features
target "prod" {
  inherits = ["base"]
  tags = [
    "${REGISTRY}devcontainer:prod-${TAG}"
  ]
  args = {
    BUILDKIT_INLINE_CACHE = "${BUILDKIT_INLINE_CACHE}"
    # Disable development dependencies in production
    PRODUCTION_BUILD = "true"
  }
  cache-from = [
    "type=local,src=/tmp/.buildx-cache",
    "type=registry,ref=${REGISTRY}devcontainer:cache-prod-${TAG}"
  ]
  cache-to = [
    "type=local,dest=/tmp/.buildx-cache-new,mode=max",
    "type=registry,ref=${REGISTRY}devcontainer:cache-prod-${TAG},mode=max"
  ]
}

# CI/CD target for automated builds
target "ci" {
  inherits = ["dev"]
  tags = [
    "${REGISTRY}devcontainer:ci-${TAG}"
  ]
  # Use GitHub Actions cache for CI builds
  cache-from = [
    "type=gha,scope=devcontainer-${TAG}",
    "type=registry,ref=${REGISTRY}devcontainer:cache-${TAG}"
  ]
  cache-to = [
    "type=gha,scope=devcontainer-${TAG},mode=max",
    "type=registry,ref=${REGISTRY}devcontainer:cache-${TAG},mode=max"
  ]
  # Enable provenance for supply chain security
  attest = [
    "type=provenance,mode=max",
    "type=sbom"
  ]
}

# Multi-platform build group
group "all" {
  targets = ["dev", "prod", "ci"]
}

# Default target
target "default" {
  inherits = ["dev"]
}