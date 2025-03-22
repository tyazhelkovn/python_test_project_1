import pytest

from python_test_project_1.lib.api.regres_api_response_service import RegresApiResponseService


@pytest.fixture(scope="session")
def regres_api_response_service():
    return RegresApiResponseService()
