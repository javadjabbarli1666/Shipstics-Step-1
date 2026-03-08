from playwright.sync_api import Page


class BasePage:
    """Base class for all Page Object Model classes."""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        """Navigate to a given URL."""
        self.page.goto(url)

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()

    def wait_for_url(self, url: str, timeout: int = 30000):
        """Wait for the page to navigate to a given URL."""
        self.page.wait_for_url(url, timeout=timeout)
