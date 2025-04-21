# app/pages/fruit.py

import reflex as rx
from ..templates.template import template
from app.FruitState import FruitScanState
from app.berry_table_state import BerryTableState
from ..components.card import card
from app.views.berry_table import berry_table
from ..views.stats_cards import stats_card


@template(
    route="/fruit",
    title="Fruit Scans",
    on_load=[FruitScanState.load_entries, BerryTableState.load_rows],
)
def fruit_page() -> rx.Component:
    return rx.vstack(
        rx.grid(
            stats_card(
                stat_name="Median Berry Size",
                value=FruitScanState.median_berry_size.to_string(),
                icon="ruler",
                icon_color="green",
            ),
            stats_card(
                stat_name="Average Berry Size",
                value=FruitScanState.average_berry_size.to_string(),
                icon="calculator",
                icon_color="blue",
            ),
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "repeat(1, 1fr)",
                "repeat(2, 1fr)",
 
            ],
            width="100%",
        ),

        # ── wrap the table in a full‑width card ────────────────
        card(
            berry_table(),
            spacing="2",
            width="100%",
        ),



    )