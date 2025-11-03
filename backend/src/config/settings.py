"""
Configuration settings for the Narrative Knowledge Graph application.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import List, Union


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Claude API Configuration
    anthropic_api_key: str = Field(..., alias="ANTHROPIC_API_KEY")

    # Neo4j Configuration
    neo4j_uri: str = Field(default="bolt://localhost:7687", alias="NEO4J_URI")
    neo4j_user: str = Field(default="neo4j", alias="NEO4J_USER")
    neo4j_password: str = Field(..., alias="NEO4J_PASSWORD")

    # API Configuration
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    api_reload: bool = Field(default=True, alias="API_RELOAD")

    # CORS Configuration
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        alias="CORS_ORIGINS"
    )

    # Application Settings
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    debug: bool = Field(default=True, alias="DEBUG")

    # Data Generation
    sample_stories_count: int = Field(default=30, alias="SAMPLE_STORIES_COUNT")

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    def get_cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [x.strip() for x in self.cors_origins.split(',')]


# Global settings instance
settings = Settings()
