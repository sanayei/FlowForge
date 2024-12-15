#!/usr/bin/env bash
set -euo pipefail

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=${AWS_DEFAULT_REGION:-us-west-2}
REPOSITORY="ocr-processor"

# Build Docker image
echo "Building Docker image..."
docker build -t ${REPOSITORY}:latest -f infrastructure/docker/Dockerfile .

# Tag image for ECR
FULL_NAME="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPOSITORY}:latest"
docker tag ${REPOSITORY}:latest ${FULL_NAME}

# Login to ECR
aws ecr get-login-password --region ${REGION} | \
    docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com

# Create repository if it doesn't exist
aws ecr describe-repositories --repository-names ${REPOSITORY} || \
    aws ecr create-repository --repository-name ${REPOSITORY}

# Push image to ECR
echo "Pushing image to ECR..."
docker push ${FULL_NAME}

echo "Image build and push complete: ${FULL_NAME}"
