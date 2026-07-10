from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str = "Project Health AI"
    app_env: str = "development"
    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 8000

    # Database (SQLite for development)
    database_url: str = "sqlite+aiosqlite:///./project_health.db"
    database_url_sync: str = "sqlite:///./project_health.db"

    # Redis (Future phases)
    redis_url: str = "redis://localhost:6379/0"

    # Logging
    log_level: str = "INFO"
    log_file_path: str = "logs/app.log"

    # Upload
    max_upload_size_mb: int = 10

    # Excel
    excel_column_mapping_path: str = "config/excel_column_mapping.yaml"

    # Future LLM
    openai_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()