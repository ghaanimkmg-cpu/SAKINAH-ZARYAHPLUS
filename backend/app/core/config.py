from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = 'development'
    DATABASE_URL: str = 'postgresql://user:password@localhost:5432/zaryah_nis'
    SECRET_KEY: str = 'change-me'
    CORS_ORIGINS: str = 'http://localhost:5173'
    KYC_SANDBOX_MODE: bool = True
    KYC_PROVIDER_BASE_URL: str = ''
    KYC_PROVIDER_API_KEY: str = ''

    class Config:
        env_file = '.env'

settings = Settings()
