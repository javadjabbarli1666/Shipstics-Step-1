from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import config


class ShipPage(BasePage):
    """Page Object Model for the Ship page — Step 1 flow."""

    PATH = "/ship"

    def __init__(self, page: Page):
        super().__init__(page)

        # Text match — stable as long as modal label doesn't change
        self.NOTICE = page.locator("//*[contains(text(),'Please note before proceeding')]")

        # Text match — resilient to DOM structure changes
        self.ACKNOWLEDGE_BUTTON = page.locator("//*[contains(text(),'I understand')]")

        # CSS class chain 
        self.SHIPMENT_FROM_TO = page.locator(
            ".flex.items-center.justify-between.\\!justify-start.type-body-5"
        )

        # aria-label — most stable for interactive controls
        self.GOLF_BAGS_INCREASE_BUTTON = page.locator(
            "(//*[@aria-label='Increase Golf Bags count'])[1]"
        )

        # Scoped input inside counter — narrowed by position [1]
        self.GOLF_BAGS_COUNT = page.locator(
            "(//*[@class='inline-flex bg-transparent mx-2 appearance-none text-center text-sm md:text-base'])[1]"
        )

        # Position-based — acceptable when no unique identifier exists on the element
        self.STANDARD_SIZE = page.locator(
            "(//*[@class='px-2 py-4 w-full flex flex-col justify-center gap-1'])[1]"
        )

        # Text match — stable as long as section label doesn't change
        self.DELIVERY_DATE = page.locator("//*[contains(text(),'Delivery Date')]")

        
        self.CALENDAR_BUTTON = page.locator("//*[contains(text(),'Please select a date')]")

        # CSS icon class — use aria-label if available on the button
        self.CALENDAR_NEXT_MONTH_BUTTON = page.locator(".icon-arrow-right.flex-shrink-0.w-5.h-5")

        # Built dynamically in select_date_for_delivery() based on scenario data
        self.CALENDAR_DATE = None

        # Text match — stable for shipping option labels
        self.GROUND_SHIPPING_OPTION = page.locator("//*[contains(text(),'Ground')]")

        # CSS scoped button — narrowed to avoid matching other Next buttons
        self.NEXT_BUTTON = page.get_by_role("button", name="Next: Traveler Details").last

        # Text match — stable for login heading
        self.LOGIN_TEXT = page.locator("//*[contains(text(),'Account Login')]")

    def open(self):
        """Navigate to ship page — URL built from config, no hardcoding."""
        self.navigate(config.BASE_URL + self.PATH)
        return self

    def acknowledge_notice(self):
        """
        Async/timing: modal appears after navigation with a delay.
        Wait for visible before clicking, then confirm it disappears
        to prevent race conditions on the next interaction.
        """
        expect(self.NOTICE).to_be_visible(timeout=10000)
        expect(self.ACKNOWLEDGE_BUTTON).to_be_enabled(timeout=10000)
        self.ACKNOWLEDGE_BUTTON.click()
        expect(self.NOTICE).to_be_hidden(timeout=10000)

    def get_shipment_from_to_text(self) -> str:
        """Return shipment route text — assertion stays in test file."""
        return self.SHIPMENT_FROM_TO.inner_text()

    def increase_golf_bags(self, times: int = 1):
        """Click increase button n times."""
        for _ in range(times):
            self.GOLF_BAGS_INCREASE_BUTTON.click()

    def get_golf_bags_count(self) -> int:
        """Return current golf bags count as integer."""
        return int(self.GOLF_BAGS_COUNT.input_value())

    def select_standard_size(self):
        """Select the standard bag size option."""
        self.STANDARD_SIZE.click()

    def select_option_delivery_date(self):
        """Select a delivery date ."""
        self.DELIVERY_DATE.click()

    def select_date_for_delivery(self, date_aria_label: str):
        """
        Async/timing: calendar has open → render → navigate → select → close
        transitions. Each step waits for the next element before proceeding.
        """
        # Build locator dynamically from scenario data — no hardcoded dates
        self.CALENDAR_DATE = self.page.locator(f"//*[@aria-label='{date_aria_label}']")

        self.CALENDAR_BUTTON.click()
        expect(self.CALENDAR_NEXT_MONTH_BUTTON).to_be_visible(timeout=5000)

        self.CALENDAR_NEXT_MONTH_BUTTON.click()
        expect(self.CALENDAR_DATE).to_be_visible(timeout=5000)

        self.CALENDAR_DATE.click()
        

    def select_ground_shipping(self):
        """
        Async/timing: shipping options load asynchronously after date selection.
        Explicit wait prevents ElementNotInteractable errors.
        """
        expect(self.GROUND_SHIPPING_OPTION).to_be_visible(timeout=15000)
        expect(self.GROUND_SHIPPING_OPTION).to_be_enabled(timeout=15000)
        self.GROUND_SHIPPING_OPTION.click()

    def click_next(self):
        """Click Next to proceed to Step 2."""
        expect(self.NEXT_BUTTON).to_be_enabled(timeout=5000)
        self.NEXT_BUTTON.click()
