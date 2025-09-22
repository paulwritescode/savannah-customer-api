# GitHub Actions Setup Guide

## 🚀 Quick Setup

### 1. Push Code to GitHub

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: Savannah Orders API"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/savanah.git
git branch -M main
git push -u origin main
```

### 2. Configure GitHub Secrets

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**

Add these repository secrets:

#### Required for CI/CD:
```
AWS_ACCESS_KEY_ID = your-aws-access-key
AWS_SECRET_ACCESS_KEY = your-aws-secret-key
AWS_ACCOUNT_ID = your-aws-account-id
```

#### Optional for production:
```
SECRET_KEY = your-production-secret-key
OIDC_CLIENT_SECRET = your-oidc-client-secret
AT_API_KEY = your-africas-talking-api-key
```

### 3. GitHub Actions Workflow

The workflow will automatically run on:
- **Push to main/develop branches**
- **Pull requests to main**

#### Workflow Steps:
1. **Test** - Run tests with SQLite
2. **Security Scan** - Check for vulnerabilities
3. **Build & Deploy** - Build Docker image and deploy to AWS (main branch only)

### 4. AWS Setup (Optional)

If you want to deploy to AWS:

1. **Create ECR Repository:**
```bash
aws ecr create-repository --repository-name savannah-orders-api --region us-east-1
```

2. **Deploy Infrastructure:**
```bash
cd infrastructure
terraform init
terraform plan
terraform apply
```

3. **Update ECS Task Definition:**
   - Update `.aws/task-definition.json` with your ECR repository URL
   - Update IAM role ARNs with your AWS account ID

### 5. Monitor Workflow

1. Go to your GitHub repository
2. Click **Actions** tab
3. View workflow runs and logs
4. Check for any failures and fix them

## 🔧 Workflow Configuration

### Test Job
- Runs on multiple Python versions (3.8-3.12)
- Uses SQLite for testing
- Generates coverage reports
- Uploads to Codecov

### Security Job
- Scans dependencies for vulnerabilities
- Uses `safety` tool

### Deploy Job (main branch only)
- Builds Docker image with SQLite
- Pushes to AWS ECR
- Deploys to ECS Fargate

## 🐛 Troubleshooting

### Common Issues:

1. **AWS Credentials Error:**
   - Check that `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are set correctly
   - Ensure AWS account ID is set

2. **ECR Repository Not Found:**
   - Create ECR repository manually
   - Update repository name in workflow

3. **ECS Service Not Found:**
   - Deploy infrastructure first with Terraform
   - Check service and cluster names

4. **Test Failures:**
   - Check test logs in Actions tab
   - Ensure all dependencies are in requirements.txt

### Debug Steps:

1. **Check workflow logs** in GitHub Actions
2. **Verify secrets** are set correctly
3. **Test locally** with same environment variables
4. **Check AWS permissions** for ECR and ECS

## 📊 Monitoring

- **Workflow Status:** GitHub Actions tab
- **Test Coverage:** Codecov integration
- **Security Issues:** Security tab in repository
- **Deployment Status:** AWS ECS console

## 🎯 Next Steps

1. **Push your code** to GitHub
2. **Set up secrets** in repository settings
3. **Monitor first workflow run**
4. **Deploy to AWS** (optional)
5. **Set up monitoring** and alerts

---

**Need help?** Check the workflow logs in GitHub Actions or create an issue in the repository.
