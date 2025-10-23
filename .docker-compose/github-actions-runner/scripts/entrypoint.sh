#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting GitHub Actions Runner for react-scuba..."

# Check if the required environment variables are set
if [ -z "$GITHUB_URL" ] || [ -z "$RUNNER_TOKEN" ]; then
  echo "Error: GITHUB_URL and RUNNER_TOKEN must be set."
  exit 1
fi

# Set defaults
RUNNER_NAME=${RUNNER_NAME:-react-scuba-runner}
RUNNER_WORKDIR=${RUNNER_WORKDIR:-/actions-runner/_work}
LABELS=${LABELS:-self-hosted,linux,x64}
RUNNER_GROUP=${RUNNER_GROUP:-Default}

echo "Configuring runner..."
echo "  GitHub URL: $GITHUB_URL"
echo "  Runner Name: $RUNNER_NAME"
echo "  Work Directory: $RUNNER_WORKDIR"
echo "  Labels: $LABELS"
echo "  Runner Group: $RUNNER_GROUP"

# Remove old runner if it exists
if [ -f ".runner" ]; then
  echo "Removing existing runner configuration..."
  ./config.sh remove --token "$RUNNER_TOKEN" || true
fi

# Configure the GitHub Actions runner
./config.sh \
  --url "$GITHUB_URL" \
  --token "$RUNNER_TOKEN" \
  --name "$RUNNER_NAME" \
  --work "$RUNNER_WORKDIR" \
  --labels "$LABELS" \
  --runnergroup "$RUNNER_GROUP" \
  --unattended \
  --replace

echo "Runner configured successfully!"
echo "Starting runner service..."

# Cleanup function
cleanup() {
  echo "Shutting down runner..."
  ./config.sh remove --token "$RUNNER_TOKEN" || true
}

# Trap SIGTERM and SIGINT
trap cleanup SIGTERM SIGINT

# Start the runner service (without --once for persistent service)
exec ./run.sh
