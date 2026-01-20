from pydantic_settings import BaseSettings


class MachingConfig(BaseSettings):
    MODEL_NAME: str = "gpt-4o-mini"


matching_config = MachingConfig()
