#!/bin/bash

# Savannah Orders API - SQLite Deployment Script

set -e

echo "🚀 Starting Savannah Orders API deployment..."

# Check if required environment variables are set
if [ -z "$AWS_REGION" ]; then
    echo "❌ AWS_REGION environment variable is required"
    exit 1
fi

if [ -z "$ECR_REPOSITORY" ]; then
    echo "❌ ECR_REPOSITORY environment variable is required"
    exit 1
fi

# Build and push Docker image
echo "📦 Building Docker image for SQLite deployment..."
docker build -t $ECR_REPOSITORY:latest .

# Tag and push to ECR
echo "🏷️  Tagging and pushing to ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

docker tag $ECR_REPOSITORY:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest

# Update ECS service
echo "🔄 Updating ECS service..."
aws ecs update-service \
    --cluster $ECS_CLUSTER \
    --service $ECS_SERVICE \
    --force-new-deployment \
    --region $AWS_REGION

echo "✅ Deployment completed successfully!"
echo "🌐 Application should be available at your ALB endpoint"
