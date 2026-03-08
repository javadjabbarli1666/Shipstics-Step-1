from dataclasses import dataclass


@dataclass
class ShipScenario:
    """Stores address and date inputs for a ship booking scenario."""
    origin: str
    destination: str
    delivery_date_aria_label: str  # Must match aria-label on calendar cell e.g. 'April 8, 2026'


# ── Scenarios ──────────────────────────────────────────────────────────────────

STANDARD_GOLF_LA_TO_MIAMI = ShipScenario(
    origin="1234 Main Street, Los Angeles, CA, USA",
    destination="4321 Main St, Miami Lakes, FL, USA",
    delivery_date_aria_label="April 8, 2026",
)


