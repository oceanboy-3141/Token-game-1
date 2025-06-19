# Google Cloud Run Deployment Guide

This guide will help you deploy the Token Game to Google Cloud Run using Google Cloud Build.

## Prerequisites

1. **Google Cloud Project**: You need a Google Cloud project with billing enabled
2. **Google Cloud SDK**: Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
3. **APIs Enabled**: Enable the following APIs:
   - Cloud Build API
   - Cloud Run API
   - Container Registry API
   - Resource Manager API

## Quick Setup

### 1. Enable Required APIs

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```

### 2. Configure Default Region (Optional)

```bash
gcloud config set run/region us-central1
```

### 3. Set Up IAM Permissions

Grant Cloud Build permissions to deploy to Cloud Run:

```bash
# Get your project number
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

# Grant Cloud Run Admin role to Cloud Build service account
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
    --role="roles/run.admin"

# Grant Service Account User role to Cloud Build service account
gcloud iam service-accounts add-iam-policy-binding \
    $PROJECT_NUMBER-compute@developer.gserviceaccount.com \
    --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"
```

## Deployment Options

### Option 1: Manual Deployment with Cloud Build

1. **Clone your repository** (if not already local):
   ```bash
   git clone <your-repo-url>
   cd token-game
   ```

2. **Submit build to Cloud Build**:
   ```bash
   gcloud builds submit --config cloudbuild.yaml .
   ```

3. **Your application will be available at**: 
   - The URL will be displayed after successful deployment
   - You can also find it in the Google Cloud Console under Cloud Run

### Option 2: Automated Deployment with Triggers

1. **Connect your repository** to Cloud Build:
   ```bash
   # For GitHub repositories
   gcloud alpha builds triggers create github \
       --repo-name=token-game \
       --repo-owner=<your-github-username> \
       --branch-pattern="^main$" \
       --build-config=cloudbuild.yaml
   ```

2. **Push to main branch** to trigger automatic deployment

### Option 3: Deploy with Alternative Configuration

If you want to customize the deployment, you can modify the `cloudbuild.yaml` file or use these manual commands:

```bash
# Build the image
gcloud builds submit --tag gcr.io/$PROJECT_ID/token-game .

# Deploy to Cloud Run
gcloud run deploy token-game \
    --image gcr.io/$PROJECT_ID/token-game \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --port 8080 \
    --max-instances 10
```

## Configuration Options

### Environment Variables

You can add environment variables during deployment:

```bash
gcloud run services update token-game \
    --set-env-vars FLASK_SECRET_KEY=your-secret-key \
    --set-env-vars FLASK_ENV=production
```

### Custom Domain

To use a custom domain:

1. **Map domain**:
   ```bash
   gcloud run domain-mappings create \
       --service token-game \
       --domain your-domain.com \
       --region us-central1
   ```

2. **Update DNS** records as instructed by the command output

### Scaling Configuration

Modify scaling settings:

```bash
gcloud run services update token-game \
    --min-instances 0 \
    --max-instances 20 \
    --concurrency 100
```

## Monitoring and Logs

### View Logs
```bash
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=token-game" --limit 50
```

### Monitor Performance
- Go to Google Cloud Console > Cloud Run > token-game
- Check the Metrics tab for performance insights

## Troubleshooting

### Common Issues

1. **Build Fails**: Check the build logs in Cloud Build console
2. **Deployment Fails**: Verify IAM permissions are correctly set
3. **App Doesn't Load**: Check that the port configuration matches (8080)
4. **Permission Denied**: Ensure the service allows unauthenticated access if needed

### Useful Commands

```bash
# Check service status
gcloud run services describe token-game --region us-central1

# View recent deployments
gcloud run revisions list --service token-game --region us-central1

# Delete service (if needed)
gcloud run services delete token-game --region us-central1
```

## Cost Optimization

- **Set minimum instances to 0** to avoid charges when not in use
- **Use appropriate memory/CPU** settings (1Gi/1 CPU should be sufficient)
- **Set reasonable timeout** values (300 seconds default)

## Security Considerations

1. **Secret Management**: Use Google Secret Manager for sensitive data
2. **Authentication**: Enable authentication if needed:
   ```bash
   gcloud run services update token-game --no-allow-unauthenticated
   ```
3. **VPC Integration**: Configure VPC connector if accessing private resources

## Next Steps

After deployment, you can:
- Set up custom monitoring and alerting
- Configure load testing
- Set up staging/production environments
- Implement CI/CD pipelines with Cloud Build triggers

For more advanced configurations, refer to the [Google Cloud Run documentation](https://cloud.google.com/run/docs). 