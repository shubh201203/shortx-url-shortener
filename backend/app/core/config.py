from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "High-Performance URL Shortener"
    MONGODB_URL: str = "mongodb://localhost:27017" # Replace with Atlas URL
    DATABASE_NAME: str = "url_shortener"
    REDIS_URL: str = "redis://localhost:6379" # Replace with Upstash URL
    FRONTEND_URL: str = "http://localhost:3000"
    JWT_SECRET: str = "change-me-in-production"

    class Config:
        env_file = ".env"

settings = Settings()
