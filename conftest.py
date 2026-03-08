import pytest
import config
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page


# ── Session scope: launched once for the entire test run ──────────────────────
@pytest.fixture(scope="session")
def browser_instance():
    """Launch browser once for the whole session, close after all tests."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=config.HEADLESS,
            slow_mo=config.SLOW_MO,
            args=["--start-maximized"],
        )
        yield browser
        browser.close()  # TEARDOWN: runs after all tests finish


# ── Function scope: fresh context per test ────────────────────────────────────
@pytest.fixture(scope="function")
def context(browser_instance: Browser):
    """Create a new browser context before each test, close after."""
    ctx = browser_instance.new_context(
        no_viewport=True,
        base_url=config.BASE_URL,
    )
    yield ctx
    ctx.close()  # TEARDOWN: runs after each test


# ── Function scope: fresh page per test ───────────────────────────────────────
@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Create a new page before each test, close after."""
    page = context.new_page()
    page.set_default_timeout(config.TIMEOUT)
    yield page
    page.close()  # TEARDOWN: runs after each test


# ── Optional: take screenshot on test failure ─────────────────────────────────
@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(page: Page, request):
    """Automatically take a screenshot if a test fails."""
    yield
    # TEARDOWN: check if test failed
    if request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False:
        path = f"screenshots/{request.node.name}.png"
        page.screenshot(path=path)
        print(f"\nScreenshot saved: {path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach test result to the request node for use in fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
