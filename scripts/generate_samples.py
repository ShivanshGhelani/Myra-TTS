"""
Sample audio generator for MyraTTS.
This script generates sample audio files in different languages for demonstration purposes.
"""

import os
import sys
import asyncio
import importlib.util
import subprocess

# Add parent directory to path to allow imports from project modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import edge_tts
from config.voice_mapping import VOICE_MAPPING_FEMALE, VOICE_MAPPING_MALE, LANGUAGE_MAPPING
from pydub import AudioSegment

# Check for required packages
required_packages = ['edge_tts', 'pydub']
missing_packages = []

for package in required_packages:
    if importlib.util.find_spec(package) is None:
        missing_packages.append(package)

if missing_packages:
    print("Error: Missing required packages:", ", ".join(missing_packages))
    print("Please install them using: pip install " + " ".join(missing_packages))
    sys.exit(1)

# Check for ffmpeg
def check_ffmpeg():
    """Check if ffmpeg is installed and accessible."""
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, 
                              check=False)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.SubprocessError):
        return False

has_ffmpeg = check_ffmpeg()
if not has_ffmpeg:
    print("Warning: ffmpeg not found. Audio will be saved as WAV files only.")
    print("To enable MP3 conversion, please install ffmpeg:")
    print("- Windows: Download from https://ffmpeg.org/download.html")
    print("- Or use: pip install ffmpeg-python")
    print("")

SAMPLES_DIR = "audio/samples"
os.makedirs(SAMPLES_DIR, exist_ok=True)

# Sample texts in different languages
SAMPLE_TEXTS = {
    "en": "Welcome to MyraTTS! This is a sample of the English voice.",
    "de": "Willkommen bei MyraTTS! Dies ist ein Beispiel der deutschen Stimme.",
    "es": "¡Bienvenido a MyraTTS! Este es un ejemplo de la voz española.",
    "fr": "Bienvenue à MyraTTS! Ceci est un exemple de la voix française.",
    "hi": "MyraTTS में आपका स्वागत है! यह हिंदी आवाज का एक नमूना है।",
    "ja": "MyraTTS へようこそ！これは日本語の声のサンプルです。",
    "ko": "MyraTTS에 오신 것을 환영합니다! 이것은 한국어 음성의 샘플입니다.",
    "ru": "Добро пожаловать в MyraTTS! Это образец русского голоса.",
    "pt": "Bem-vindo ao MyraTTS! Este é um exemplo da voz portuguesa.",
    "it": "Benvenuto in MyraTTS! Questo è un esempio di voce italiana."
}

async def generate_sample(lang_code, text, voice_name, output_filename):
    """Generate a sample audio file using edge-tts."""
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(output_filename)
    
    # Convert to MP3 to save space if ffmpeg is available
    if output_filename.endswith('.wav') and has_ffmpeg:
        try:
            mp3_filename = output_filename.replace('.wav', '.mp3')
            audio = AudioSegment.from_wav(output_filename)
            audio.export(mp3_filename, format="mp3", bitrate="192k")
            os.remove(output_filename)  # Remove WAV file
            print(f"Converted {os.path.basename(output_filename)} to MP3")
        except Exception as e:
            print(f"Warning: Could not convert {os.path.basename(output_filename)} to MP3: {str(e)}")
            print("Keeping WAV format instead.")

async def main():
    """Generate sample audio files in different languages."""
    tasks = []
    
    # Choose selected languages for samples (to keep the repository size reasonable)
    selected_langs = ["en", "es", "fr", "de", "ja"]
    
    for lang_code in selected_langs:
        if lang_code in SAMPLE_TEXTS and lang_code in VOICE_MAPPING_FEMALE:
            text = SAMPLE_TEXTS[lang_code]
            
            # Female voice sample
            female_voice = VOICE_MAPPING_FEMALE[lang_code]
            female_output = os.path.join(SAMPLES_DIR, f"{lang_code}_female.wav")
            tasks.append(generate_sample(lang_code, text, female_voice, female_output))
            
            # Male voice sample (if available)
            if lang_code in VOICE_MAPPING_MALE:
                male_voice = VOICE_MAPPING_MALE[lang_code]
                male_output = os.path.join(SAMPLES_DIR, f"{lang_code}_male.wav")
                tasks.append(generate_sample(lang_code, text, male_voice, male_output))
    
    await asyncio.gather(*tasks)
    print(f"Generated {len(tasks)} sample audio files in {SAMPLES_DIR}")

if __name__ == "__main__":
    asyncio.run(main())
