from dotenv import load_dotenv
import os

load_dotenv()

SERVER_URL = 'localhost'
PORT = '8900'
ENV = 'dev'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
DEFAULT_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3002",
    "http://localhost:5173",
    "https://ia-calculator-frontend.vercel.app",
    "https://ia-calculator-frontend-git-main-johan-garcia-trejos-projects.vercel.app",
]
ENV_CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]
CORS_ORIGINS = list(dict.fromkeys([*DEFAULT_CORS_ORIGINS, *ENV_CORS_ORIGINS]))
CORS_ORIGIN_REGEX = os.getenv("CORS_ORIGIN_REGEX", r"https://.*\.vercel\.app")
