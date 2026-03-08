from playwright.sync_api import Page


class BasePage:
    """Base class for all Page Object Model classes."""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        """Navigate to a given URL."""
        self.page.goto(url)
