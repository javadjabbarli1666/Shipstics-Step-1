import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.ship_page import ShipPage
from test_data import STANDARD_GOLF_LA_TO_MIAMI


class TestShipPageStep1:

    def test_step1_full_flow(self, page: Page):
        """
        Setup: complete home page flow to land on the ship page.
        autouse=True ensures this runs before every test in this class.
        """
        # ── Scenario: swap this to change addresses and date ──────────────
        scenario = STANDARD_GOLF_LA_TO_MIAMI
        # ──────────────────────────────────────────────────────────────────

        home = HomePage(page)
        home.open()
        home.select_one_way()
        home.enter_origin(scenario.origin)
        home.enter_destination(scenario.destination)
        home.click_get_started()

        self.ship = ShipPage(page)
        # Async/timing: modal appears after navigation — wait and dismiss
        self.ship.acknowledge_notice()

        # Assertion 1: Origin city is shown in the route summary.
        # Assertion 2: Destination city is shown in the route summary.
        route_text = self.ship.get_shipment_from_to_text()

        # Extract city names from scenario addresses (e.g. "1234 Main Street, Los Angeles, CA, USA" → "Los Angeles")
        origin_city = scenario.origin.split(", ")[1]
        destination_city = scenario.destination.split(", ")[1]

        assert origin_city in route_text, (
            f"Expected '{origin_city}' in route but got: '{route_text}'"
        )
        assert destination_city in route_text, (
            f"Expected '{destination_city}' in route but got: '{route_text}'"
        )

        # Assertion 3: Counter increments by the correct amount.
        # Async/timing: wait for DOM to reflect updated input value after click.
        initial_count = self.ship.get_golf_bags_count()

        self.ship.increase_golf_bags(times=1)

        # Wait for DOM to update before reading the new value
        expect(self.ship.GOLF_BAGS_COUNT).not_to_have_value(
            str(initial_count), timeout=5000
        )

        updated_count = self.ship.get_golf_bags_count()
        assert updated_count == initial_count + 1, (
            f"Expected {initial_count + 1} bags but got {updated_count}"
        )

        # Full Step 1 flow: size -> date (async) -> shipping (async) -> next.
        # Assertion 4: Shipping options load and ground is visible.
        # Assertion 5: Login screen appears after completing Step 1.
        self.ship.select_standard_size()
        
        

        # Async/timing: calendar open -> navigate month -> select date -> close
        self.ship.select_date_for_delivery(scenario.delivery_date_aria_label)

        # Async/timing: shipping options load after date selection
        self.ship.select_ground_shipping()

        # Assertion 5: ground shipping option is visible after async load
        expect(self.ship.GROUND_SHIPPING_OPTION).to_be_visible()

        self.ship.click_next()

        page.wait_for_timeout(2000)  # pause to inspect state after next click

        # Assertion 6: login page appears after completing Step 1
        expect(self.ship.LOGIN_TEXT).to_be_visible(timeout=10000)
