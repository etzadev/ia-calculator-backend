from dotenv import load_dotenv
import os

load_dotenv()

SERVER_URL = 'localhost'
PORT = '8900'
ENV = 'dev'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:3002,http://localhost:5173,"
        "https://ia-calculator-frontend-git-main-johan-garcia-trejos-projects.vercel.app",
    ).split(",")
    if origin.strip()
]
