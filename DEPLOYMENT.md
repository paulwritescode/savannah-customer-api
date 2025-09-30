# AWS App Runner Deployment Guide

## 🚀 Deploy to AWS App Runner

### Prerequisites
1. AWS Account with appropriate permissions
2. GitHub repository with your code
3. AWS CLI configured (optional, can use AWS Console)

### Step 1: Push Code to GitHub
```bash
git add .
git commit -m "Add App Runner deployment configuration"
git push origin main
```

### Step 2: Create App Runner Service

#### Option A: Using AWS Console (Recommended)
1. Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner/)
2. Click "Create service"
3. Choose "Source": "Source code repository"
4. Connect your GitHub account
5. Select your repository: `savanah`
6. Choose branch: `main`
7. Configure build settings:
   - **Build command**: `docker build -t savannah-orders-api .`
   - **Start command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
8. Configure service settings:
   - **Service name**: `savannah-orders-api`
   - **Port**: `8000`
   - **Environment variables** (add these):
     ```
     DATABASE_URL=sqlite:///./data/savannah_orders.db
     SECRET_KEY=your-production-secret-key-here
     AT_USERNAME=sandbox
     AT_API_KEY=your-africas-talking-api-key
     DEBUG=false
     ```
9. Click "Create & deploy"

#### Option B: Using AWS CLI
```bash
# Create apprunner.yaml (already created)
# Then create the service
aws apprunner create-service \
  --service-name savannah-orders-api \
  --source-configuration '{
    "AutoDeploymentsEnabled": true,
    "CodeRepository": {
      "RepositoryUrl": "https://github.com/YOUR_USERNAME/savanah",
      "SourceCodeVersion": {
        "Type": "BRANCH",
        "Value": "main"
      },
      "CodeConfiguration": {
        "ConfigurationSource": "REPOSITORY",
        "CodeConfigurationValues": {
          "Runtime": "DOCKER",
          "BuildCommand": "docker build -t savannah-orders-api .",
          "StartCommand": "uvicorn app.main:app --host 0.0.0.0 --port 8000"
        }
      }
    }
  }' \
  --instance-configuration '{
    "Cpu": "0.25 vCPU",
    "Memory": "0.5 GB"
  }'
```

### Step 3: Configure Auto-Deployment
1. In App Runner console, go to your service
2. Click "Configuration" tab
3. Under "Source", enable "Auto deployments"
4. This will automatically deploy on every push to main branch

### Step 4: Set Environment Variables
1. Go to your App Runner service
2. Click "Configuration" tab
3. Under "Environment variables", add:
   ```
   DATABASE_URL=sqlite:///./data/savannah_orders.db
   SECRET_KEY=your-secure-production-secret-key
   AT_USERNAME=sandbox
   AT_API_KEY=your-africas-talking-api-key
   AT_SENDER_ID=SAVANNAH
   DEBUG=false
   ```

### Step 5: Access Your API
1. After deployment completes (5-10 minutes), you'll get a URL like:
   `https://xyz123.us-east-1.awsapprunner.com`
2. Test your API:
   ```bash
   curl https://your-app-runner-url.awsapprunner.com/health
   curl https://your-app-runner-url.awsapprunner.com/docs
   ```

## 🔄 Automatic Deployment
Once configured, every push to the `main` branch will:
1. Trigger GitHub Actions (CI)
2. Automatically deploy to App Runner (CD)
3. Update your live API

## 💰 Cost Considerations
- App Runner charges based on usage
- Small API like this: ~$5-10/month
- Free tier: 2000 build minutes/month

## 🛠️ Troubleshooting
- Check App Runner logs in AWS Console
- Ensure all environment variables are set
- Verify Dockerfile builds locally first
- Check GitHub repository permissions

## 🔒 Security Notes
- Change `SECRET_KEY` to a secure random string
- Use environment variables for sensitive data
- Consider using AWS Secrets Manager for production
