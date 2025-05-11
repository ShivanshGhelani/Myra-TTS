# Deployment Guide

This document provides step-by-step instructions to deploy MyraTTS on both Vercel and GitHub.

## 1. Deploy on Vercel

### Prerequisites
- [Vercel account](https://vercel.com/signup)
- [Vercel CLI](https://vercel.com/docs/cli) (optional)

### Steps

1. **Fork or clone the repository**

2. **Create a new project in Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New" > "Project"
   - Import your GitHub repository or upload the project files

3. **Configure project settings**
   - Framework Preset: Other
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: `pip install -r requirements.txt`
   - Root Directory: `/`

4. **Deploy**
   - Click "Deploy"
   - Wait for the deployment to complete

5. **Update Vercel URL in the project**
   - After successful deployment, copy your Vercel URL (e.g., `https://myra-tts.vercel.app`)
   - Run the update script:
     ```
     python scripts/update_vercel_url.py https://your-vercel-url.vercel.app
     ```
   - Commit and push the changes

## 2. Set up GitHub Repository

1. **Create a new repository on GitHub**
   - Go to [GitHub](https://github.com/new)
   - Name the repository (e.g., `MyraTTS`)
   - Choose whether to make it public or private
   - Click "Create repository"

2. **Initialize Git and push to GitHub**
   ```bash
   # Initialize git repository
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit"
   
   # Add remote
   git remote add origin https://github.com/your-username/MyraTTS.git
   
   # Push to GitHub
   git push -u origin main
   ```

3. **Update GitHub URL in the project**
   ```bash
   python scripts/update_repo_url.py https://github.com/your-username/MyraTTS
   ```

4. **Commit and push the update**
   ```bash
   git add config/deployment.py
   git commit -m "Update GitHub repository URL"
   git push
   ```

## 3. Continuous Deployment

Once both GitHub and Vercel are set up, you can enable continuous deployment:

1. **Link Vercel to GitHub repository**
   - In your Vercel project settings, connect to your GitHub repository
   - Enable automatic deployments on push to main branch

2. **Test continuous deployment**
   - Make a small change to your repository
   - Push the change to GitHub
   - Vercel should automatically deploy the updated version

## 4. Additional Configuration

### Environment Variables

If your application requires environment variables:

1. **Add them in Vercel**
   - Go to your project in the Vercel dashboard
   - Click "Settings" > "Environment Variables"
   - Add your key-value pairs

### Custom Domain

To use a custom domain with your Vercel deployment:

1. **Add custom domain**
   - Go to your project in the Vercel dashboard
   - Click "Settings" > "Domains"
   - Add your custom domain and follow the verification steps
