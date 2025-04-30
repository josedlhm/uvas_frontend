# app/ui/pages/fruit.py
import reflex as rx

from app.ui.layouts.shell import template
from app.ui.state.fruit import FruitScanState
from app.ui.state.berry_table import BerryTableState
from app.ui.components.card import card
from app.ui.components.stats_cards import stats_card
from app.ui.components.berry_distribution_chart import berry_size_distribution_chart
from app.ui.components.berry_table import berry_table

@template(
    route="/fruit",
    title="Fruit Scans",
    on_load=[
        FruitScanState.load_upload_options,
        FruitScanState.load_entries,
        BerryTableState.load_rows,
    ],
)
def fruit_page() -> rx.Component:
    return rx.vstack(        

        # ── Upload ID dropdown with full “Upload ID: {value}” text ────────
        rx.hstack(
            rx.select.root(
                # This trigger shows our custom label + the current value
                rx.select.trigger(
                    rx.hstack(
                        rx.text("Upload ID:", size="4", weight="medium"),
                        rx.text(FruitScanState.filter_upload_id, size="4", weight="medium"),
                        spacing="2",
                    ),
                    size="3",
                    variant="surface",
                    radius = "large"
                ),
                # The dropdown list of raw IDs
                rx.select.content(
                    rx.select.group(
                        rx.foreach(
                            FruitScanState.upload_options,
                            lambda upload_id, _: rx.select.item(
                                upload_id, value=upload_id
                            ),
                        )
                    )
                ),
                # Fully controlled props
                value=FruitScanState.filter_upload_id,
                on_change=FruitScanState.set_filter_upload_id,
            ),
            width="100%",
        ),

        # ── Stats cards ────────────────────────────────────────────
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
            grid_template_columns=["1fr", "1fr", "repeat(2, 1fr)"],
            gap="1rem",
            width="100%",
            spacing = "4"
        ),

        # ── Chart & table ────────────────────────────────────────
        card(berry_size_distribution_chart(), spacing="2", width="100%"),
        card(berry_table(), spacing="2", width="100%"),

        spacing = "8"


    )
