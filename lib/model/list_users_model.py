from typing import List

from pydantic import StrictInt, StrictStr

from lib.model.base_model import BaseTestModel


class Data(BaseTestModel):
    id: StrictInt
    email: StrictStr
    first_name: StrictStr
    last_name: StrictStr
    avatar: StrictStr


class Support(BaseTestModel):
    url: StrictStr
    text: StrictStr


class UsersSchema(BaseTestModel):
    page: StrictInt
    per_page: StrictInt
    total: StrictInt
    total_pages: StrictInt
    data: List[Data]
    support: Support
