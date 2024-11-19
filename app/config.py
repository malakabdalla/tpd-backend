import os
from dotenv import load_dotenv
import logging

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)