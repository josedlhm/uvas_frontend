import reflex as rx
from app.ui.state.fruit import FruitScanState

def berry_size_distribution_chart() -> rx.Component:
    """
    Area chart showing berry-size distribution (histogram).
    Uses FruitScanState.size_distribution as data.
    """
    return rx.vstack(
        # Chart title
        rx.heading("Berry Size Distribution", size="5", align="left"),

        # Area chart with tooltip, legend, and axis labels
        rx.recharts.area_chart(
            # Show tooltips on hover
            rx.recharts.graphing_tooltip(),
            # Display legend with series name

            # Filled area representing berry counts
            rx.recharts.area(
                data_key="count",
                name="Berry Count",
                type_="monotone",
            ),
            # X-axis: bins of berry size
            rx.recharts.x_axis(
                data_key="bin",
                name="Size",
                label={"value": "Size (mm)", "position": "insideBottom", "offset": -5},
            ),
           
            data=FruitScanState.size_distribution,
            width="100%",
            height=250,
            margin={"top": 10, "right": 30, "left": 0, "bottom": 10},
        ),
        spacing="1",
        width="100%",
    )
