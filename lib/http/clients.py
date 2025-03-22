from lib.configuration.config import config
from lib.http.base_http_client import BaseHttpClient


class RegresApiClient(BaseHttpClient):
    def __init__(self):
        super().__init__(config.REGRES_API_URL)