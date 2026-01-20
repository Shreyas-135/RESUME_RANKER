from pydantic_settings import BaseSettings


class CandidateConfig(BaseSettings):
    MODEL_NAME: str = "gpt-4o-mini"

    CV_UPLOAD_DIR: str = "./candidate_cv/"


candidate_config = CandidateConfig()
