from pydantic import BaseModel, Extra


class BaseTestModel(BaseModel):
    class Config:
        extra = Extra.forbid