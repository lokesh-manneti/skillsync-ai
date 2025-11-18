from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

class Settings(BaseSettings):
    # Pydantic will automatically read from environment variables
    # No model_config is needed for this default behavior
    
    # Database
    DATABASE_URL: str

    # Google AI
    GOOGLE_API_KEY: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

# Create a single instance to be imported elsewhere
settings = Settings()