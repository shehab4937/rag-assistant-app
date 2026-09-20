from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    ollama_host: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3:latest"

    chroma_path: str = "data/vector_store/uniguide_chroma"
    chroma_collection: str = "uniguide_documents"

    embedding_model: str = "all-MiniLM-L6-v2"

    frontend_origin: str = "http://localhost:4200"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @property
    def chroma_absolute_path(self) -> Path:
        path = Path(self.chroma_path)

        if path.is_absolute():
            return path

        return BASE_DIR / path


settings = Settings()