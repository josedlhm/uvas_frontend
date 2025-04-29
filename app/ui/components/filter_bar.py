import reflex as rx
from typing import Callable, List

def filter_bar(
    *,
    label: str,
    items: rx.Var[List[str]],
    value: rx.Var[str],
    on_change: Callable[[str], None],
    width: str = "12rem",
) -> rx.Component:
    """
    A pill-style filter control:
    - label on the left
    - outlined select with down-chevron
    """
    return rx.hstack(
        # Label text
        rx.text(label, size="4", weight="medium"),
        # The dropdown
        rx.select(
            items,
            value=value,
            on_change=on_change,
            variant="classic",        # pill border
            radius="full",            # fully rounded
            size="3",                 
            width=width,
            icon=rx.icon("chevron-down", size=16),
        ),
        spacing="2",
        align="center",
    )
