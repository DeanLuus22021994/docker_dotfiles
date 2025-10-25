#!/bin/bash
# LocalStack initialization script
# Creates default AWS resources for local development

set -e

echo "Initializing LocalStack AWS services..."

# Wait for LocalStack to be ready
until curl -s http://localhost:4566/_localstack/health | grep -q "running"; do
    echo "Waiting for LocalStack to be ready..."
    sleep 2
done

echo "LocalStack is ready, creating resources..."

# Create default S3 buckets
awslocal s3 mb s3://local-dev-bucket 2>/dev/null || echo "S3 bucket already exists"
awslocal s3 mb s3://local-test-bucket 2>/dev/null || echo "S3 bucket already exists"

# Create DynamoDB tables
awslocal dynamodb create-table \
    --table-name local-dev-table \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    2>/dev/null || echo "DynamoDB table already exists"

# Create SQS queues
awslocal sqs create-queue --queue-name local-dev-queue 2>/dev/null || echo "SQS queue already exists"

# Create SNS topics
awslocal sns create-topic --name local-dev-topic 2>/dev/null || echo "SNS topic already exists"

echo "LocalStack initialization complete!"
