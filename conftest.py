import os
import pytest
from playwright.sync_api import sync_playwright
from conf import pytest_addoption

Base_Dir = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1440,
            "height": 1080
        },
        "ignore_https_errors": True,
        "record_video_dir": os.path.join(Base_Dir, "videos")
    }


