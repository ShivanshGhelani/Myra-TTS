import os
import edge_tts
import io
import logging
from langdetect import detect
from enum import Enum
from config.voice_mapping import VOICE_MAPPING, VOICE_MAPPING_MALE, VOICE_MAPPING_FEMALE, DEFAULT_VOICE, DEFAULT_VOICE_MALE
from config.settings import settings

# Setup logger
logger = logging.getLogger(__name__)

class VoiceGender(str, Enum):
    MALE = "male"
    FEMALE = "female"

def detect_language(text: str) -> str:
    """Detect the language of the input text."""
    try:
        return detect(text)
    except:
        return "en"

async def text_to_speech(text: str) -> str:
    """Legacy function: Convert text to speech and save to file."""
    lang = detect_language(text)
    voice = VOICE_MAPPING.get(lang, "en-US-JennyNeural")

    if os.path.exists(settings.SPEECH_FILE_PATH):
        try:
            os.remove(settings.SPEECH_FILE_PATH)
        except PermissionError:
            pass

    communicate = edge_tts.Communicate(text, voice, pitch='+5Hz', rate='+13%')
    await communicate.save(settings.SPEECH_FILE_PATH)

    return settings.SPEECH_FILE_PATH

async def text_to_speech_stream(text: str, voice_gender: VoiceGender = VoiceGender.FEMALE):
    """Convert text to speech and return audio data as a BytesIO buffer."""
    if not text:
        raise ValueError("Text cannot be empty")
        
    try:
        # Clean and validate the input text
        cleaned_text = ' '.join(text.split()).strip()
        if not cleaned_text:
            raise ValueError("Text contains no valid characters")

        if len(cleaned_text) > 5000:
            raise ValueError("Text is too long (max 5000 characters)")        # Detect language and select voice
        detected_lang = detect_language(cleaned_text)
        voice_mapping = VOICE_MAPPING_MALE if voice_gender == VoiceGender.MALE else VOICE_MAPPING_FEMALE
        
        # Check if the detected language is supported
        is_supported = detected_lang in voice_mapping
        
        # Use gender-appropriate default voice if language is not supported
        default_voice = DEFAULT_VOICE_MALE if voice_gender == VoiceGender.MALE else DEFAULT_VOICE
        voice = voice_mapping.get(detected_lang, default_voice)
        
        logger.info(f"TTS request - Text: '{cleaned_text[:100]}...', Language: {detected_lang}, Supported: {is_supported}, Voice: {voice}, Gender: {voice_gender}")
        
        # If language is not supported, add this info to the log
        if not is_supported:
            logger.warning(f"Unsupported language detected: {detected_lang}. Using default voice for gender {voice_gender}: {voice}")
        
        # Configure TTS parameters based on content
        is_single_word = len(cleaned_text.split()) == 1
        communicate = edge_tts.Communicate(
            text=f"{cleaned_text} " if is_single_word else cleaned_text,  # Add space for single words
            voice=voice,
            rate="-20%" if is_single_word else "+10%",  # Slower for single words
            volume="+0%",  # Consistent volume
            pitch="+0Hz" if is_single_word else "+5Hz"  # Neutral pitch for words
        )
        
        if not communicate:
            raise ValueError("Failed to create TTS communicator")
            
        # Stream and collect audio data
        audio_buffer = io.BytesIO()
        audio_size = 0
        has_audio = False
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                chunk_data = chunk["data"]
                audio_size += len(chunk_data)
                
                # Check for reasonable audio size
                if audio_size > 10 * 1024 * 1024:  # 10MB limit
                    raise ValueError("Generated audio is too large")
                    
                audio_buffer.write(chunk_data)
                has_audio = True
        
        if not has_audio:
            raise ValueError("No audio was generated")
            
        # Validate final audio data
        audio_buffer.seek(0)
        audio_data = audio_buffer.getvalue()
        if not audio_data or len(audio_data) < 100:  # Minimum size check
            raise ValueError("Generated audio is invalid or corrupted")
            
        # Return valid audio buffer
        audio_buffer.seek(0)
        return audio_buffer
            
    except Exception as e:
        logger.error(f"TTS error: {str(e)}, Voice: {voice if 'voice' in locals() else 'unknown'}, Gender: {voice_gender}, Lang: {detected_lang if 'detected_lang' in locals() else 'unknown'}")
        raise
