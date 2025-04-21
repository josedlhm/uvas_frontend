import reflex as rx
from ..templates.template import template


@template(route="/fruit", title="Fruit Scans")

def fruit_page():
    return rx.box(
        rx.heading("Fruit Scans"),
        rx.text(
            "Welcome to the Fruit page. Here you can view and analyze your fruit scan data.",
        ),
        width="100%",
    )
