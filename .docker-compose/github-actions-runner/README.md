# GitHub Actions Self-Hosted Runner for react-scuba

This project provides a self-hosted GitHub Actions runner service using Docker for the [react-scuba](https://github.com/DeanLuus22021994/react-scuba) repository. The runner is configured with minimal footprint and uses named volume mounts for persistence across builds.

## Features

- ✨ **Minimal Footprint**: Built on Ubuntu 22.04 with only essential dependencies
- 🔄 **Persistent Storage**: Uses named Docker volumes for work directory, configuration, and credentials
- 🔒 **Secure**: Runs as non-root user inside the container
- 🚀 **Auto-restart**: Configured with `restart: unless-stopped` for reliability
- 📊 **Resource Limits**: CPU and memory limits to prevent resource exhaustion
- 🏷️ **Custom Labels**: Easy workflow targeting with custom runner labels

## Project Structure

- `docker-compose.yml`: Defines the runner service with named volumes for persistence
- `Dockerfile`: Builds a minimal Ubuntu 22.04 image with GitHub Actions runner v2.329.0
- `scripts/entrypoint.sh`: Configuration and startup script with proper cleanup handling
- `.env.example`: Template for environment variables with defaults for react-scuba

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 1.29 or higher)
- A GitHub repository with admin access to register self-hosted runners

## Setup Instructions

### 1. Get a Runner Token

Go to your repository settings to get a new runner token:

```text
https://github.com/DeanLuus22021994/react-scuba/settings/actions/runners/new
```

**Note**: Runner tokens expire after 1 hour, so generate a new one each time you set up or reconfigure the runner.

### 2. Configure Environment Variables

Copy the `.env.example` file to `.env` and add your runner token:

```bash
cp .env.example .env
```

Edit `.env` and set your `RUNNER_TOKEN`:

```bash
RUNNER_TOKEN=YOUR_ACTUAL_TOKEN_HERE
```

### 3. Build and Start the Runner

Build the Docker image and start the runner service:

```bash
docker-compose up -d --build
```

### 4. Verify the Runner

Check the logs to ensure the runner started successfully:

```bash
docker-compose logs -f
```

You should see messages indicating successful configuration and "Listening for Jobs".

Verify in GitHub:

```text
https://github.com/DeanLuus22021994/react-scuba/settings/actions/runners
```

## Usage in Workflows

Use this runner in your GitHub Actions workflows by specifying:

```yaml
jobs:
  build:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      # Your workflow steps here
```

Or target specific labels:

```yaml
jobs:
  build:
    runs-on: [self-hosted, linux, react, scuba]
    steps:
      - uses: actions/checkout@v4
      # Your workflow steps here
```

## Volume Persistence

The runner uses three named volumes for persistence:

- **react_scuba_runner_work**: Stores workflow job data and build artifacts
- **react_scuba_runner_config**: Stores runner configuration
- **react_scuba_runner_credentials**: Stores authentication credentials

These volumes persist across container restarts and rebuilds.

## Management Commands

### View logs

```bash
docker-compose logs -f
```

### Stop the runner

```bash
docker-compose down
```

### Restart the runner

```bash
docker-compose restart
```

### Remove everything (including volumes)

```bash
docker-compose down -v
```

### Rebuild after changes

```bash
docker-compose up -d --build
```

## Resource Limits

The runner is configured with:

- **CPU Limit**: 2 cores maximum
- **Memory Limit**: 2GB maximum
- **CPU Reservation**: 1 core minimum
- **Memory Reservation**: 1GB minimum

Adjust these in `docker-compose.yml` based on your needs.

## Troubleshooting

### Runner not appearing in GitHub

1. Check if the token has expired (tokens expire after 1 hour)
2. Verify the GitHub URL is correct in `.env`
3. Check logs: `docker-compose logs -f`

### Runner keeps restarting

1. Check logs for error messages
2. Ensure the token is valid
3. Verify network connectivity to GitHub

### Out of disk space

1. Clean up old Docker volumes: `docker volume prune`
2. Remove unused images: `docker image prune -a`
3. Check volume usage: `docker system df -v`

## Security Considerations

- The runner operates as a non-root user inside the container
- Never commit your `.env` file with actual tokens to version control
- Regenerate runner tokens regularly
- Monitor runner activity in GitHub repository settings
- Consider using runner groups for organization-level control

## Additional Information

- [GitHub Actions Self-Hosted Runners Documentation](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners)
- [Runner Release Notes](https://github.com/actions/runner/releases/tag/v2.329.0)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
