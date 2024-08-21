from pydantic_settings import SettingsConfigDict, BaseSettings 


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encode='utf-8'
    )
    DATABASE_URL: str