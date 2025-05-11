from fastapi import FastAPI, HTTPException, APIRouter, Request, Response
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel, field_validator
import asyncio
import io
import logging
import re
from pydub import AudioSegment
import base64

# Import core TTS functionality
from core.tts import text_to_speech_stream, detect_language, VoiceGender

router = APIRouter()
logger = logging.getLogger(__name__)

class TTSRequest(BaseModel):
    text: str
    voice_gender: VoiceGender = VoiceGender.FEMALE

    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError("Text cannot be empty")
        
        # Remove any non-printable characters
        cleaned = ''.join(char for char in v if char.isprintable())
        # Remove multiple spaces
        cleaned = ' '.join(cleaned.split())
        return cleaned

    @property
    def cleaned_text(self):
        return self.text.strip()

@router.post("/tts")
async def text_to_speech(request: TTSRequest):
    """Convert text to speech and return audio data."""
    try:
        if not request.cleaned_text:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Detect language first
        detected_lang = detect_language(request.cleaned_text)
        
        # Check if language is supported in voice mapping
        from config.voice_mapping import VOICE_MAPPING_MALE, VOICE_MAPPING_FEMALE
        voice_mapping = VOICE_MAPPING_MALE if request.voice_gender == VoiceGender.MALE else VOICE_MAPPING_FEMALE
        is_language_supported = detected_lang in voice_mapping
        
        logger.info(f"Processing TTS request with text: {request.cleaned_text}, language: {detected_lang}, supported: {is_language_supported}, voice gender: {request.voice_gender}")
        audio_data = await text_to_speech_stream(request.cleaned_text, request.voice_gender)
        
        if audio_data.getvalue():
            return Response(
                content=audio_data.getvalue(),
                media_type="audio/mp3",
                headers={
                    "X-Detected-Language": detected_lang,
                    "X-Language-Supported": str(is_language_supported).lower(),
                    "Content-Disposition": 'attachment; filename="audio.mp3"'
                }
            )
        else:
            raise HTTPException(status_code=500, detail="No audio was generated")
    except Exception as e:
        logger.error(f"TTS generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



class DownloadRequest(BaseModel):
    """Model for TTS download request validation."""
    text: str
    format: str = "mp3"
    voice_gender: str = "female"

    @field_validator("text")
    @classmethod
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError("Text cannot be empty")
        return v.strip()

    @field_validator("format")
    @classmethod
    def validate_format(cls, v):
        v = v.lower()
        if v not in ["mp3", "wav", "ogg"]:
            raise ValueError("Format must be one of: mp3, wav, ogg")
        return v

    @field_validator("voice_gender")
    @classmethod
    def validate_voice_gender(cls, v):
        v = v.lower()
        if v not in ["male", "female"]:
            return "female"
        return v

@router.post("/tts/download")
async def download_audio(request: DownloadRequest):
    """Convert text to speech and download in specified format."""
    try:
        # Generate audio using core function
        voice_gender = VoiceGender.MALE if request.voice_gender == "male" else VoiceGender.FEMALE
        
        # Detect language and check if supported
        detected_lang = detect_language(request.text)
        from config.voice_mapping import VOICE_MAPPING_MALE, VOICE_MAPPING_FEMALE
        voice_mapping = VOICE_MAPPING_MALE if voice_gender == VoiceGender.MALE else VOICE_MAPPING_FEMALE
        is_language_supported = detected_lang in voice_mapping
        
        audio_data = await text_to_speech_stream(request.text, voice_gender)
        
        if not audio_data or not audio_data.getvalue():
            raise HTTPException(
                status_code=500, 
                detail="Failed to generate audio data"
            )

        # Set content type and filename based on format
        content_types = {
            "wav": "audio/wav",
            "mp3": "audio/mpeg",
            "ogg": "audio/ogg"
        }
        content_type = content_types.get(request.format, "audio/mpeg")
        filename = f"speech.{request.format}"

        # Return the audio file as a downloadable response
        return Response(
            content=audio_data.getvalue(),
            media_type=content_type,
            headers={
                "X-Detected-Language": detected_lang,
                "X-Language-Supported": str(is_language_supported).lower(),
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the audio file"
        )

# Note: TextToSpeechRequest removed as it was duplicate of GenerateSpeechRequest
class GenerateSpeechRequest(BaseModel):
    text: str
    voice: str = "female"  # Default to female voice

    @field_validator('voice')
    @classmethod
    def validate_voice(cls, v):
        if v.lower() not in ['male', 'female']:
            raise ValueError("Voice must be either 'male' or 'female'")
        return v.lower()

    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError("Text cannot be empty")
        return v.strip()

@router.post("/generate-speech")
async def generate_speech(request: GenerateSpeechRequest):
    """
    Generate speech from text with specified voice gender.
    Example request body:
    {
        "text": "Hello world",
        "voice": "female"
    }
    """
    try:
        # Convert voice string to VoiceGender enum
        voice_gender = VoiceGender.MALE if request.voice == "male" else VoiceGender.FEMALE
        
        # Detect language first
        detected_lang = detect_language(request.text)
        
        # Check if language is supported
        from config.voice_mapping import VOICE_MAPPING_MALE, VOICE_MAPPING_FEMALE
        voice_mapping = VOICE_MAPPING_MALE if voice_gender == VoiceGender.MALE else VOICE_MAPPING_FEMALE
        is_language_supported = detected_lang in voice_mapping
        
        logger.info(f"Processing speech generation request: text='{request.text}', language={detected_lang}, supported={is_language_supported}, voice={request.voice}")
        
        # Generate audio from core function
        audio_data = await text_to_speech_stream(request.text, voice_gender)
        
        if not audio_data.getvalue():
            raise HTTPException(status_code=500, detail="Failed to generate audio")
            
        # Return the audio response with detected language header
        return Response(
            content=audio_data.getvalue(),
            media_type="audio/mp3",
            headers={
                "X-Detected-Language": detected_lang,
                "X-Language-Supported": str(is_language_supported).lower(),
                "Content-Disposition": 'attachment; filename="speech.mp3"'
            }
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Speech generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

