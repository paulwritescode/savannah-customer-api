# CI Setup Guide

## Quick Start - CI Only

To start with **CI only** (testing and linting without deployment), follow these steps:

### 1. Use the CI-Only Workflow

I've created a dedicated CI-only workflow at `.github/workflows/ci-only.yml` that:
- ✅ Tests on Python 3.8, 3.9, 3.10, 3.11, 3.12
- ✅ Runs linting with flake8
- ✅ Runs tests with coverage
- ✅ Performs security scanning
- ✅ Tests Docker build (without deployment)
- ❌ **No AWS deployment** (CI only)

### 2. Disable the Full CI/CD Pipeline

To use only CI without deployment, you can either:

**Option A: Rename the files**
```bash
# Rename the full CI/CD to disable it
mv .github/workflows/ci-cd.yml .github/workflows/ci-cd.yml.disabled

# Keep only the CI-only workflow
# .github/workflows/ci-only.yml (already exists)
```

**Option B: Modify the trigger**
Edit `.github/workflows/ci-cd.yml` and change the trigger to only run on specific branches:
```yaml
on:
  push:
    branches: [deploy-only]  # Only runs on 'deploy-only' branch
  pull_request:
    branches: [main]
```

### 3. Push to GitHub

```bash
git add .
git commit -m "Add CI-only workflow"
git push origin main
```

### 4. Check GitHub Actions

1. Go to your GitHub repository
2. Click on "Actions" tab
3. You should see "CI Only (Testing & Linting)" workflow
4. Click on it to see the progress

## What the CI-Only Workflow Does

### Test Job
- Tests on multiple Python versions (3.8-3.12)
- Installs dependencies
- Runs linting with flake8
- Runs tests with pytest and coverage
- Uploads coverage reports to Codecov

### Security Scan Job
- Installs safety package
- Scans requirements.txt for vulnerabilities

### Build Test Job
- Tests Docker build
- Tests container startup
- Tests health endpoint
- Cleans up test containers

## Troubleshooting

### If you see "Python 3.1" error:
This is likely a cached issue. Try:
1. Clear GitHub Actions cache
2. Push a new commit
3. Or delete and recreate the workflow file

### If tests fail:
1. Check the "Actions" tab for detailed logs
2. Look for specific error messages
3. Run tests locally first: `pytest`

### If you want to add deployment later:
1. Rename `.github/workflows/ci-cd.yml.disabled` back to `.github/workflows/ci-cd.yml`
2. Configure AWS secrets in GitHub repository settings
3. Push to main branch to trigger deployment

## Next Steps

1. **Start with CI-only** to ensure everything works
2. **Fix any test failures** locally first
3. **Add deployment** when you're ready for AWS

The CI-only workflow will give you confidence that your code is working before adding the complexity of deployment! 🚀
