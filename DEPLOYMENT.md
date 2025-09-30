# AWS App Runner Deployment Guide

## 🚀 Deploy to AWS App Runner

### Configuration File Approach
This project uses the **configuration file approach** where App Runner reads all settings from `apprunner.yaml` in your repository root. This is the recommended approach because:

- ✅ **Version controlled**: Configuration is stored in your repository
- ✅ **Automatic**: No manual configuration needed in AWS Console
- ✅ **Consistent**: Same configuration across environments
- ✅ **Easy updates**: Change configuration by updating the file

### Understanding apprunner.yaml
The `apprunner.yaml` file contains all the configuration App Runner needs:

```yaml
version: 1.0
runtime: docker                    # Use Docker runtime
build:
  commands:
    build:
      - docker build -t savannah-orders-api .  # Build command
run:
  runtime-version: latest
  command: uvicorn app.main:app --host 0.0.0.0 --port 8000  # Start command
  network:
    port: 8000                    # Port to expose
    env: PORT                     # Environment variable for port
  env:                           # Environment variables
    - name: DATABASE_URL
      value: "sqlite:///./data/savannah_orders.db"
    - name: SECRET_KEY
      value: "your-production-secret-key-change-this"
    # ... more environment variables
```

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

#### Option A: Using AWS Console with Configuration File (Recommended)
1. Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner/)
2. Click "Create service"
3. Choose "Source": "Source code repository"
4. Connect your GitHub account
5. Select your repository: `savanah`
6. Choose branch: `main`
7. **Important**: Leave "Source directory" empty (uses root directory)
8. Choose "Configuration file" for build settings
9. **App Runner will automatically read from `apprunner.yaml`**
10. Configure service settings:
    - **Service name**: `savannah-orders-api`
    - **Auto deployments**: Enable for automatic deployment on push
11. Click "Create & deploy"

**Note**: App Runner will automatically use the configuration from `apprunner.yaml` in your repository root.

#### Option B: Using AWS CLI with Configuration File
```bash
# App Runner will automatically read from apprunner.yaml
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
        "ConfigurationSource": "REPOSITORY"
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

### Step 4: Update Environment Variables (Optional)
**Note**: Environment variables are already configured in `apprunner.yaml`. If you need to override them:

1. Go to your App Runner service
2. Click "Configuration" tab
3. Under "Environment variables", you can override the values from `apprunner.yaml`:
   ```
   SECRET_KEY=your-secure-production-secret-key
   AT_API_KEY=your-actual-africas-talking-api-key
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
