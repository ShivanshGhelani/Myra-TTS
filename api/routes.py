from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routes import tts
from api import repository

router = APIRouter()
templates = Jinja2Templates(directory="templates")


router.include_router(tts.router, tags=["tts"])
router.include_router(repository.router, prefix="/api", tags=["repository"])
