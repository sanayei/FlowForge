#!/usr/bin/env bash
set -euo pipefail

# Initialize Terraform
echo "Initializing Terraform..."
cd infrastructure/terraform
terraform init

# Plan deployment
echo "Planning deployment..."
terraform plan -out=tfplan

# Apply deployment
echo "Applying deployment..."
terraform apply tfplan

echo "Deployment complete!"