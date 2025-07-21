from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    API_PREFIX: str = "/"
    DEBUG: bool = True
    DATABASE_URL: str
    ALLOWED_ORIGINS: str = ""

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str):
        # return v.split(",") if v else []
        return ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_senstive = True


settings = Settings()
