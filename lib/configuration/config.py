from pydantic import BaseSettings


class Config(BaseSettings):
    REGRES_API_URL: str = "https://reqres.in"


config = Config()