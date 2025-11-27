from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, MongoDsn, Field
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings managed by Pydantic.
    Reads from environment variables and .env file.
    """
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" # Ignore extra fields in .env
    )

    # Required fields (will raise error if missing)
    OPENAI_API_KEY: SecretStr
    MONGO_URI: str # Changed from MongoDsn because Pydantic adds port 27017 which breaks SRV
    
    # Optional fields with defaults
    LANGFUSE_PUBLIC_KEY: Optional[str] = None
    LANGFUSE_SECRET_KEY: Optional[SecretStr] = None
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"
    
    # App configuration
    ENVIRONMENT: str = Field(default="development", pattern="^(development|staging|production)$")
    DEBUG: bool = False

# Singleton instance
settings = Settings()
