import reflex as rx
from app.ui.layouts.shell import template
from app.ui.components.card import card
from app.ui.state.plant import PlantScanState

from app.ui.components.stats_cards import stats_card

from app.ui.components.bunch_table import bunch_table
from app.ui.state.bunch_table import BunchTableState


class PlantPageState(rx.State):
    @rx.event
    def init_page(self):
        # Load both the stats and the table in one go:
        return [
            PlantScanState.load_entries(),   # your existing KPI loader
            BunchTableState.load_rows(),     # the new table loader
        ]


@template(
    route="/plant",
    title="Plant Scans",
    on_load=PlantPageState.init_page,
)
def plant_page() -> rx.Component:
    return rx.vstack(
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
                "1fr",
                "repeat(1, 1fr)",
                "repeat(2, 1fr)",
                "repeat(3, 1fr)",
                "repeat(3, 1fr)",
            ],
            width="100%",
        ),
        card(

        bunch_table(),

        spacing="2",
        width="100%",
    )
    )
