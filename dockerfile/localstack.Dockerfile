# LocalStack Dockerfile - Local AWS cloud stack
# Emulates AWS services for local development and testing

FROM localstack/localstack:latest

# Install additional AWS CLI tools
USER root

RUN apk add --no-cache \
    python3 \
    py3-pip \
    curl \
    jq \
    bash \
    aws-cli \
    docker-cli

# Install AWS SAM CLI
RUN pip3 install --no-cache-dir \
    aws-sam-cli \
    awscli-local \
    boto3 \
    botocore

# Copy initialization scripts
COPY dockerfile/configs/localstack-init.sh /etc/localstack/init/ready.d/init.sh
RUN chmod +x /etc/localstack/init/ready.d/init.sh

# Create localstack directories
RUN mkdir -p /tmp/localstack \
    && mkdir -p /var/lib/localstack \
    && chown -R localstack:localstack /tmp/localstack /var/lib/localstack

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=5 \
    CMD curl -f http://localhost:4566/_localstack/health || exit 1

USER localstack

# Expose LocalStack ports
EXPOSE 4566 4571

# Volume for persistence
VOLUME ["/var/lib/localstack"]

# Start LocalStack
CMD ["localstack", "start"]
