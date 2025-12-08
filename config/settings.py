from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """애플리케이션 전체 설정"""

    # MySQL URL (필수)
    MYSQL_URL: str

    # OpenAI Settings (필수)
    OPENAI_API_KEY: str

    # Redis Settings (선택 - 기본값 localhost)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    REDIS_URL: str | None = None

    # Server Settings
    BASE_URL: str = "http://localhost:8000"  # production에서는 도메인으로

    # Google OAuth Settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def database_url(self) -> str:
        """SQLAlchemy용 URL 반환 (mysql:// -> mysql+pymysql://)"""
        if self.MYSQL_URL.startswith("mysql://"):
            return self.MYSQL_URL.replace("mysql://", "mysql+pymysql://", 1)
        return self.MYSQL_URL


@lru_cache()
def get_settings() -> Settings:
    """설정 싱글톤 반환 (캐싱)"""
    return Settings()