FROM ubuntu:22.04

ENV RUNNER_VERSION=2.329.0
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies for minimal footprint
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  curl \
  ca-certificates \
  git \
  jq \
  libicu70 \
  && rm -rf /var/lib/apt/lists/*

# Create a non-root user for the runner
RUN useradd -m -s /bin/bash runner

# Create a directory for the GitHub Actions runner
RUN mkdir -p /actions-runner && chown -R runner:runner /actions-runner

# Set the working directory
WORKDIR /actions-runner

# Download and extract the GitHub Actions runner
RUN curl -o actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz -L \
  https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz && \
  echo "194f1e1e4bd02f80b7e9633fc546084d8d4e19f3928a324d512ea53430102e1d  actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz" | sha256sum -c && \
  tar xzf ./actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz && \
  rm actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz && \
  ./bin/installdependencies.sh && \
  chown -R runner:runner /actions-runner

# Copy the entrypoint script
COPY scripts/entrypoint.sh /actions-runner/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /actions-runner/entrypoint.sh

# Switch to non-root user
USER runner

# Set the entrypoint
ENTRYPOINT ["/actions-runner/entrypoint.sh"]
