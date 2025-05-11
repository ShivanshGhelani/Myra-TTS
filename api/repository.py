from fastapi import APIRouter
from config.deployment import GITHUB_REPOSITORY_URL

router = APIRouter()

@router.get("/repository-url")
async def get_repository_url():
    """
    Returns the GitHub repository URL for the project.
    This will be empty until the repository is created and configured.
    """
    return {"url": GITHUB_REPOSITORY_URL}
