import allure


def equals(expected, actual):
    with allure.step(f"Assert that {expected} equals {actual}"):
        assert expected == actual, f"expected {expected} not equals {actual}"

def not_equals(expected, actual):
    with allure.step(f"Assert that {expected} not equals {actual}"):
        assert expected != actual, f"expected {expected} equals {actual}"

def not_empty(actual):
    with allure.step("Assert entity is not empty"):
        assert len(actual) != 0, f"expected {actual} not empty"