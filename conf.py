import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="stage",
        help="Environment to run tests against"
    )


@pytest.fixture(scope="session")
def env(pytestconfig):
    return pytestconfig.getoption("--env")


@pytest.fixture(scope="session")
def base_url(env):
    if env == "stage":
        return "https://example.stage.meetwhale.com"
    elif env == "prod":
        return "https://example.com"
    else:
        raise ValueError("Invalid environment")
