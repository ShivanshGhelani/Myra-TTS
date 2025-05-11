# MyraTTS - Modern Text-to-Speech Web Application

A sleek, responsive web application that converts text to natural-sounding speech using advanced AI technology.

## Features

- 🎙️ High-quality text-to-speech conversion
- 🌐 Support for 25+ languages with automatic language detection
- 👨‍👩‍👧‍👦 Multiple voice options (male/female)
- 📱 Fully responsive design for all devices (mobile, tablet, desktop)
- ♿ Accessibility features built-in
- 🎵 Interactive audio visualizer
- 💾 Download options (MP3, WAV)

## Live Demo

[Check out the live demo](https://myra-tts.vercel.app)

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **TTS Engine**: Microsoft Edge TTS
- **Deployment**: Vercel

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/MyraTTS.git
cd MyraTTS
```

2. Quick Setup (Windows):
```bash
# For PowerShell:
.\install_dependencies.ps1

# For Command Prompt:
install_dependencies.bat
```

3. Manual Setup:
```bash
python -m venv myra_tts
source myra_tts/bin/activate  # On Windows: myra_tts\Scripts\activate
pip install -r requirements.txt
```

4. Generate Sample Audio (optional):
```bash
# PowerShell:
.\scripts\run_generate_samples.ps1

# Command Prompt:
scripts\run_generate_samples.bat
```

5. Run the application:
```bash
uvicorn api.main:create_app --reload
```

5. Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

## Deployment

This application is configured for deployment on Vercel. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

For beginners, a step-by-step guide is available in [STEP_BY_STEP_GUIDE.md](STEP_BY_STEP_GUIDE.md).

## Helper Scripts

MyraTTS comes with several utility scripts to help you manage the project:

- `install_dependencies.ps1` / `install_dependencies.bat` - Install all required dependencies
- `scripts/generate_samples.py` - Generate sample audio files in multiple languages
- `scripts/update_repo_url.py` - Update the GitHub repository URL after creating your repo
- `scripts/update_vercel_url.py` - Update the Vercel deployment URL after deploying
- `scripts/init_project.py` - Initialize the project (virtual environment, dependencies)

## License

MIT License - See [LICENSE](LICENSE) file for details

## Acknowledgements

- Microsoft Edge TTS for the speech synthesis
- Font Awesome for icons
