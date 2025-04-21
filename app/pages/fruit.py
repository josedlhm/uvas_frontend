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
        # ── 1) stats cards ───────────────────────────────
        rx.grid(
            # two cards only
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
            grid_template_columns=[
                "1fr",            # base
                "1fr",            # sm
                "repeat(2, 1fr)"  # md, lg, xl all get 2 columns
            ],
            gap="1rem",

            # make sure the grid itself stretches the entire content width
            width="100%",
            
        ),

        # ── 2) berry table ───────────────────────────────
        card(
            berry_table(),
            spacing="2",
            width="100%",
        ),

        # ── 3) force this VStack to stretch too ────────


    )
