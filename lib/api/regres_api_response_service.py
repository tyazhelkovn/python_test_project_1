from lib.http.base_http_client import HttpMethod
from lib.http.clients import RegresApiClient


class RegresApiResponseService:
    def __init__(self):
        self.client = RegresApiClient()

    def get_user_list(self, page: int = 0):
        return self.client.make_request(
            path_url="/api/users",
            query={"page": page},
            http_method=HttpMethod.GET
        )