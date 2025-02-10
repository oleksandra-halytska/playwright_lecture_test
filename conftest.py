import os
import re
from pathlib import Path

import pytest
from playwright.sync_api import Playwright, expect
from slugify import slugify
import allure
from allure_commons.types import AttachmentType


@pytest.fixture
def main_page(playwright):
    browser = playwright.chromium.launch()
    context = browser.new_context(locale='en-US')
    page = context.new_page()
    page.goto("https://first.institute/edu/")

    yield page
    browser.close()


@pytest.fixture
def hello_task_page(page):
    # browser = playwright.chromium.launch()
    # context = browser.new_context(locale='en-US')
    # page = context.new_page()
    output = page.locator("#output")
    editor_content = page.get_by_role("textbox", name="Editor content")
    page.goto("https://first.institute/edu/course/basic_python/task/hello_stranger/")

    expect(output).not_to_be_empty()
    page.wait_for_selector("#output")
    expect(output).to_have_value(re.compile(r"Python 3\.12\.7 ready\."))
    expect(editor_content).not_to_be_empty()

    yield page


@pytest.fixture
def make_page_fixture(hello_task_page) -> object:
    def make(page_name):
        if page_name == "hello_task_page":
            return hello_task_page
        else:
            raise ValueError(f"Unknown page: {page_name}")
    return make


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()

    if result.failed:
        page = item.funcargs.get("page", None)
        if page:
            screenshot_bytes = page.screenshot()

            allure.attach(
                screenshot_bytes,
                attachment_type=AttachmentType.PNG
            )
