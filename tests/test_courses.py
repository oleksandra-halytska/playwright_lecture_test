import re
from playwright.sync_api import Playwright, expect
from tests.pages.course_card import all_cards
from tests.test_data import TESTED_FUNCTION, FUNCTION_CALL


def test_courses(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://first.institute/edu/")

    cards = all_cards(page)
    card, *_ = cards

    assert len(cards) == 1, "Очікується рівно 1 картка"
    assert card.title == "Знайомство з Python", "Заголовок картки некоректний"


def test_output_verification(make_page_fixture: callable) -> None:
    page = make_page_fixture("hello_task_page")

    page.get_by_text("Run").click()
    expect(page.locator("#output")).to_have_value(re.compile(r"Привіт"))


def test_custom_code_verification(make_page_fixture: callable) -> None:
    page = make_page_fixture("hello_task_page")
    editor_content = page.get_by_role("textbox", name="Editor content")
    output = page.locator("#output")

    editor_content.press('Meta+A')
    editor_content.press("Delete")
    expect(editor_content).to_be_empty()

    editor_content.fill(TESTED_FUNCTION)
    editor_content.fill(FUNCTION_CALL)

    page.get_by_text("Run").click()
    expect(output).to_have_value(re.compile(r"\nS\na\ns\nh\na\n"))
