from pydantic_settings import BaseSettings
from typing import List, Union
import os

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "postgresql://postgres.ljweyghvntlakotdrxmm:thunderboltRG@18@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
    
    # Supabase Configuration
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    
    # JWT Configuration
    JWT_SECRET_KEY: str = "RTieB23m9poj6ctsjHDLxHQ6gzlu1NJEII71IdwgMJwfalzsub/NSYq9KIQL6zENyEENAGVoPuX//cRR7ujEtg=="
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App Configuration
    APP_NAME: str = "Hoodie Store API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS Configuration
    ALLOWED_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "https://your-frontend-domain.vercel.app"
    ]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Handle ALLOWED_ORIGINS if it comes as a string from environment
        if isinstance(self.ALLOWED_ORIGINS, str):
            self.ALLOWED_ORIGINS = [origin.strip() for origin in self.ALLOWED_ORIGINS.split(',')]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
