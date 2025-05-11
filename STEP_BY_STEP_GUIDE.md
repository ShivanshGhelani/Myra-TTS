# Step-by-Step Deployment Guide for MyraTTS

## Deploying to Vercel First

1. **Sign up for Vercel**
   - Go to https://vercel.com/signup
   - Create an account (you can sign up with GitHub)

2. **Install Vercel CLI (optional)**
   ```powershell
   npm i -g vercel
   ```

3. **Deploy to Vercel**
   
   **Option A: Using the Vercel Dashboard (Recommended for beginners)**
   - Go to https://vercel.com/new
   - Import your project from GitHub (or upload the files directly)
   - Configure the project:
     - Framework preset: Other
     - Build Command: Leave blank
     - Output Directory: Leave blank
     - Install Command: `pip install -r requirements.txt`
     - Root Directory: `/`
   - Click "Deploy"

   **Option B: Using the Vercel CLI**
   ```powershell
   # Navigate to your project directory
   cd s:\Projects\FastAPI\SeperateFolder\MyraTTS
   
   # Login to Vercel
   vercel login
   
   # Deploy
   vercel
   ```

4. **Update the Vercel URL in your project**
   ```powershell
   python scripts/update_vercel_url.py https://your-vercel-url.vercel.app
   ```

## Creating and Setting Up GitHub Repository

1. **Create a new repository on GitHub**
   - Go to https://github.com/new
   - Name your repository (e.g., "MyraTTS")
   - Choose public or private
   - Do not initialize with README, .gitignore, or license
   - Click "Create repository"

2. **Initialize Git in your local project**
   ```powershell
   cd s:\Projects\FastAPI\SeperateFolder\MyraTTS
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. **Connect to GitHub and push**
   ```powershell
   git remote add origin https://github.com/your-username/MyraTTS.git
   git branch -M main
   git push -u origin main
   ```

4. **Update the GitHub repository URL in your project**
   ```powershell
   python scripts/update_repo_url.py https://github.com/your-username/MyraTTS
   ```

5. **Commit and push the updated config**
   ```powershell
   git add config/deployment.py
   git commit -m "Update GitHub repository URL"
   git push
   ```

## Setting Up Continuous Deployment

1. **Connect Vercel to your GitHub repository**
   - Go to your project in the Vercel dashboard
   - Click on "Settings" > "Git"
   - Click "Connect" next to GitHub
   - Select your repository
   - Configure the settings (similar to step 3 of deploying to Vercel)
   - Enable "Auto Deploy" option

2. **Make changes and see automatic deployments**
   - Any push to your main branch will trigger a new deployment

## Completing Setup

1. **Generate sample audio files (optional)**
   ```powershell
   python scripts/generate_samples.py
   ```

2. **Commit and push the sample files**
   ```powershell
   git add audio/samples/
   git commit -m "Add sample audio files"
   git push
   ```

3. **Test the deployed application**
   - Open your Vercel URL in a browser
   - Try the text-to-speech functionality
   - Check if the GitHub repository link works

## Next Steps

1. **Customize the README**
   - Update the README.md with your specific details
   - Add screenshots of your application

2. **Set up a custom domain (optional)**
   - In Vercel dashboard: Project > Settings > Domains
   - Add your custom domain and follow the verification steps

3. **Add environment variables if needed**
   - In Vercel dashboard: Project > Settings > Environment Variables
