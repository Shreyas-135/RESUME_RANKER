from pydantic_settings import BaseSettings


class JobConfig(BaseSettings):
    MODEL_NAME: str = "gpt-4o-mini"


job_config = JobConfig()
