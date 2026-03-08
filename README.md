# ShipStics – Python Playwright UI Testing Project

A UI test automation project using **Python**, **Playwright**, and **pytest** following the **Page Object Model (POM)** pattern.

## Project Structure

```
.
├── conftest.py          # pytest fixtures (browser, context, page, screenshot on failure)
├── config.py            # Playwright settings (base URL, headless, timeout, viewport)
├── pytest.ini           # pytest configuration and HTML report output
├── requirements.txt     # Python dependencies
├── test_data.py         # ShipScenario dataclass — stores origin, destination, delivery date
├── .gitignore           # Excludes cache, screenshots, reports, venv
├── .github/
│   └── workflows/
│       └── playwright.yml  # GitHub Actions CI workflow
├── pages/
│   ├── __init__.py
│   ├── base_page.py     # Base POM class with shared methods (navigate, title, screenshot)
│   ├── home_page.py     # Home page POM (trip type, origin, destination, get started)
│   └── ship_page.py     # Ship page POM (Step 1: bags, date, shipping, next)
├── tests/
│   ├── __init__.py
│   └── test_ship_page.py # Ship page Step 1 full flow test
├── reports/
│   └── report.html      # Auto-generated HTML test report (after test run)
└── screenshots/         # Auto-captured on test failure
```

## Prerequisites

- Python 3.9+
- pip

## Setup

1. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

2. Install Playwright browsers:
   ```bash
   python3 -m playwright install chromium
   ```

## Running Tests

Run all tests with the VS Code task **"Run Playwright Tests"**, or via terminal:

```bash
python3 -m pytest tests/ -v
```

Run a specific test file:

```bash
python3 -m pytest tests/test_ship_page.py -v
```

## Configuration

Edit `config.py` to adjust:
- `BASE_URL` – the URL under test
- `HEADLESS` – run browsers headlessly (`True`) or visually (`False`)
- `TIMEOUT` – default action timeout in milliseconds
- `VIEWPORT` – browser window dimensions

## CI – GitHub Actions

The workflow at `.github/workflows/playwright.yml` runs automatically on every push and pull request to `main`/`master`, and can also be triggered manually from the **Actions** tab.

| Step | What it does |
|---|---|
| Checkout | Clones the repository |
| Setup Python 3.12 | Installs Python with pip cache |
| Install dependencies | `pip install -r requirements.txt` |
| Install Chromium | `playwright install chromium --with-deps` |
| Run tests | `pytest tests/ -v` with `HEADLESS=true` |
| Upload report | Attaches `reports/report.html` as an artifact (14 days) |
| Upload screenshots | Attaches `screenshots/` on failure (7 days) |

> **Headless mode**: `config.py` reads the `HEADLESS` environment variable. CI sets it to `true`; locally it defaults to `false` (headed).

## Adding New Pages

1. Create a new file in `pages/`, e.g. `pages/login_page.py`
2. Inherit from `BasePage`
3. Define locators and interaction methods
4. Write tests in `tests/test_login_page.py`

## Guidelines

- Keep assertions in test files, **not** in page objects
- Use fixtures from `conftest.py` for browser/context/page setup
- Follow `test_*.py` naming for test files and `Test*` for test classes
