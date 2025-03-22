import pytest
import allure

from lib.model.list_users_model import UsersSchema
from lib.utils import check
from lib.utils.asserts import equals, not_empty


@pytest.mark.regresapi
@allure.title("Getting and verifying the allowed number of users")
def test_per_page_users(regres_api_response_service):
    user_list_response = regres_api_response_service.get_user_list(page=1)
    check.ok_response(response=user_list_response, schema=UsersSchema)
    user_list = user_list_response.json()
    per_page = user_list["per_page"]
    user_data_length = len(user_list["data"])
    equals(per_page, user_data_length)


@pytest.mark.regresapi
@allure.title("Getting and checking the total number of users on all pages")
def test_total_users(regres_api_response_service):
    user_list_response = regres_api_response_service.get_user_list(page=1)
    check.ok_response(response=user_list_response, schema=UsersSchema)
    user_list = user_list_response.json()
    user_total = user_list["total"]
    user_total_pages = user_list["total_pages"]
    user_length = 0

    for page in range(1, user_total_pages + 1):
        user_list_response_by_page = regres_api_response_service.get_user_list(page=page)
        user_length += len(user_list_response_by_page.json()["data"])

    equals(user_total, user_length)


@pytest.mark.regresapi
@allure.title("Getting and verifying the matching number of pages")
def test_pages_users(regres_api_response_service):
    user_list_response = regres_api_response_service.get_user_list(page=1)
    check.ok_response(response=user_list_response, schema=UsersSchema)
    user_list = user_list_response.json()
    user_total_pages = user_list["total_pages"]

    for page in range(1, user_total_pages + 1):
        user_list_response_by_page = regres_api_response_service.get_user_list(page=page).json()
        equals(page, user_list_response_by_page["page"])
        not_empty(user_list_response_by_page["data"])
