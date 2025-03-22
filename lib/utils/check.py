import json

import allure

from pydantic import ValidationError
from requests import Response


@allure.step("API response checking")
def ok_response(response: Response, schema = None):
    if response.status_code not in (200, 201):
        raise AssertionError(f"Response failed with status code: {response.status_code}")
    if schema is not None:
        _check_schema(response, schema)


def _check_schema(response: Response, schema):
    if _check_is_response_json(response):
        request_name = f"[{response.request.method}] <{response.request.url}>"
        with allure.step(f"Validating response schema for: {request_name}"):
            try:
                schema.parse_obj(response.json())
            except ValidationError as e:
                allure.attach(
                    json.dumps(e.errors(), indent=4, ensure_ascii=False),
                    "Response schema validation errors",
                    allure.attachment_type.JSON
                )
                raise AssertionError(f"Response failed schema validation: {request_name}")


def _check_is_response_json(response: Response) -> bool:
    response_type = response.headers.get("Content-Type")
    return response_type is not None and response_type.lower().startswith("application/json")