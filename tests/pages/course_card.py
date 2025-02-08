from dataclasses import dataclass
from playwright.sync_api import Page


@dataclass
class CourseCard:
    course_url: str
    img_url: str
    title: str
    description: str
    learn_button_url: str


def all_cards(page: Page) -> list[CourseCard]:
    cards = page.locator("div.card").all()
    course_cards = []

    for card in cards:
        course_url = card.locator("a").first.get_attribute("href")
        img_url = card.locator("img").get_attribute("src")
        title = card.locator(".card-title a").inner_text()
        description = card.locator(".card-text").inner_text()
        learn_button_url = card.locator(".btn.btn-secondary").get_attribute(
            "href")

        course_cards.append(
            CourseCard(
                course_url=course_url,
                img_url=img_url,
                title=title,
                description=description,
                learn_button_url=learn_button_url
            )
        )

    return course_cards
