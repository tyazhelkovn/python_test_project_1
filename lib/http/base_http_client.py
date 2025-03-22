import uuid

import allure

from enum import Enum
from typing import Optional
from requests import Session, Request, RequestException

from lib.utils.to_curl import to_curl


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class BaseHttpClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def make_request(self, path_url: str = "",
                     http_method: HttpMethod = HttpMethod.GET,
                     headers: Optional[dict] = None,
                     query: Optional[dict] = None,
                     body: Optional[dict] = None
                     ):
        full_url = self.base_url + path_url

        if headers is None:
            headers = {}

        debug_request_id = str(uuid.uuid4())
        headers.update({
            "X-Request-Id": debug_request_id
        })

        with Session() as session:
            raw_request = Request(
                method=http_method,
                url=full_url,
                headers=headers,
                json=body,
                params=query
            )

            prepared_request = raw_request.prepare()

            with allure.step(f"Request [{http_method}]: <{full_url}>"):

                allure.attach(to_curl(prepared_request), "Curl")
                allure.attach(debug_request_id, "RequestID")

                try:
                    response = session.send(
                        request=prepared_request,
                        verify=False
                    )
                except RequestException as err:
                    if "response" in err.args[0].__dict__:
                        allure.attach(
                            name="Retried last status code",
                            body=str(err.args[0].response.status),
                            attachment_type=allure.attachment_type.TEXT
                        )
                        allure.attach(
                            name="Retried last response",
                            body=err.args[0].response.data.decode("utf-8"),
                            attachment_type=allure.attachment_type.TEXT
                        )
                    else:
                        allure.attach(
                            name="Retried last error",
                            body=str(err),
                            attachment_type=allure.attachment_type.TEXT
                        )
                    raise

                return response
