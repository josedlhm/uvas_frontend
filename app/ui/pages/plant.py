# app/ui/pages/plant.py
import reflex as rx

from app.ui.layouts.shell import template
from app.ui.state.plant import PlantScanState
from app.ui.state.bunch_table import BunchTableState
from app.ui.components.card import card
from app.ui.components.stats_cards import stats_card
from app.ui.components.bunch_table import bunch_table

class PlantPageState(rx.State):
    @rx.event
    def init_page(self):
        return [
            PlantScanState.load_upload_options,
            PlantScanState.load_entries,
            BunchTableState.load_rows,
        ]

@template(
    route="/plant",
    title="Plant Scans",
    on_load=[
        PlantScanState.load_upload_options,
        PlantPageState.init_page,
    ],
)
def plant_page() -> rx.Component:
    return rx.vstack(
        # ── Upload ID dropdown with full “Upload ID: {value}” text ────────
        rx.hstack(
            rx.select.root(
                # This trigger shows our custom label + the current value
                rx.select.trigger(
                    rx.hstack(
                        rx.text("Upload ID:", size="4", weight="medium"),
                        rx.text(PlantScanState.filter_upload_id, size="4", weight="medium"),
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
                            PlantScanState.upload_options,
                            lambda upload_id, _: rx.select.item(
                                upload_id, value=upload_id
                            ),
                        )
                    )
                ),
                # Fully controlled props
                value=PlantScanState.filter_upload_id,
                on_change=PlantScanState.set_filter_upload_id,
            ),
            width="100%",
            padding_bottom="1em",
        ),

        # ── Stats cards ────────────────────────────────────────────
        rx.grid(
            stats_card(
                stat_name="Total Grape Bunches",
                value=PlantScanState.total_bunches,
                icon="grape",
                icon_color="purple",
            ),
            stats_card(
                stat_name="Median Visible Berries per Bunch",
                value=PlantScanState.median_berries.to_string(),
                icon="cherry",
                icon_color="green",
            ),
            stats_card(
                stat_name="Median Estimated Berries per Bunch",
                value=PlantScanState.median_berries.to_string(),
                icon="eye",
                icon_color="red",
            ),
            gap="1rem",
            grid_template_columns=[
                "1fr", "repeat(1, 1fr)", "repeat(2, 1fr)", "repeat(3, 1fr)"
            ],
            width="100%",
        ),

        # ── Bunch table ────────────────────────────────────────────
        card(
            bunch_table(),
            spacing="2",
            width="100%",
        ),
    )
