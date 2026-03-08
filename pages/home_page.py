from playwright.sync_api import Page
from pages.base_page import BasePage
import config


class HomePage(BasePage):
    """Page Object Model for the Home page."""

    PATH = "/"

    # Locators
    
    NAV_LINKS = "nav a"

    def __init__(self, page: Page):
        super().__init__(page)

        # Text match — stable as long as heading copy doesn't change
        self.HEADING_TEXT = page.locator("//*[contains(text(),'Skip Baggage Claim.')]")

        self.TRIP_TYPE_OPTIONS = page.locator("//*[@aria-haspopup='listbox']")

        self.ONE_WAY_BUTTON = page.locator("//*[contains(text(),'One way')]")

        # placeholder text — stable identifier for search inputs
        self.ORIGIN_INPUT = page.get_by_placeholder("Where from?")

        # placeholder text — stable identifier for destination input
        self.DESTINATION_INPUT = page.get_by_placeholder("Where to?")

        # Text match scoped to first match — avoids matching footer links
        self.GET_STARTED_BUTTON = page.locator("(//*[contains(text(),'Get started')])[1]")



    def open(self):
        """Open the home page."""
        self.navigate(config.BASE_URL + self.PATH)
        return self

    def get_heading_text(self) -> str:
        """Return the main heading text."""
        return self.HEADING_TEXT.first.inner_text()

    def select_one_way(self):
        """Select the one-way trip option."""
        self.TRIP_TYPE_OPTIONS.click()
        self.ONE_WAY_BUTTON.click()

    def enter_origin(self, origin: str):
        """Type origin and wait for autocomplete suggestion, then select first result."""
        self.ORIGIN_INPUT.fill(origin)
        # Async/timing: wait for dropdown — exclude hidden class, target only visible options
        first_option = self.page.locator("[role='option']:not(.hidden)").first
        first_option.wait_for(state="visible", timeout=10000)
        # Small delay to allow the UI to fully render before clicking
        self.page.wait_for_timeout(500)
        first_option.click()

    def enter_destination(self, destination: str):
        """Type destination and wait for autocomplete suggestion, then select first result."""
        self.DESTINATION_INPUT.fill(destination)
        # Async/timing: wait for dropdown — exclude hidden class, target only visible options
        first_option = self.page.locator("[role='option']:not(.hidden)").first
        first_option.wait_for(state="visible", timeout=10000)
        # Small delay to allow the UI to fully render before clicking
        self.page.wait_for_timeout(500)
        first_option.click()

    def click_get_started(self):
        """Click the 'Get Started' button."""
        self.GET_STARTED_BUTTON.click()