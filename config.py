# Playwright configuration settings
import os

BASE_URL = "https://app.staging.shipsticks.com"

BROWSER = "chromium"  # Options: chromium, firefox, webkit

# CI sets HEADLESS=true via environment variable; locally defaults to False
HEADLESS = os.environ.get("HEADLESS", "false").lower() == "true"

SLOW_MO = 0  # Milliseconds to slow down Playwright operations (useful for debugging)

TIMEOUT = 30000  # Default timeout in milliseconds

VIEWPORT = {
    "width": 1920,
    "height": 1080,
}

SCREENSHOTS_DIR = "screenshots"

TRACES_DIR = "traces"
