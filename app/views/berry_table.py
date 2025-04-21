# app/views/berry_table.py

import reflex as rx
from app.berry_table_state import BerryTableState, BerryRow

# ─── header & row renderers ──────────────────────────────────────────
def _berry_header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(rx.icon(icon, size=18), rx.text(text), spacing="2", align="center")
    )

def _show_berry_row(row: BerryRow, index: int) -> rx.Component:
    bg    = rx.cond(index % 2 == 0, rx.color("gray", 1), rx.color("accent", 2))
    hover = rx.cond(index % 2 == 0, rx.color("gray", 3), rx.color("accent", 3))
    return rx.table.row(
        rx.table.row_header_cell(row.bunch_id),
        rx.table.cell(row.berry_id),
        rx.table.cell(f"{row.berry_size:.1f}"),
        style={"_hover": {"bg": hover}, "bg": bg},
        align="center",
    )

def _berry_pagination_view() -> rx.Component:
    S = BerryTableState
    return rx.hstack(
        rx.text("Page ", rx.code(S.page_number), f" of {S.total_pages}"),
        rx.hstack(
            rx.icon_button(
                rx.icon("chevrons-left", size=18),
                on_click=S.first_page,
                opacity=rx.cond(S.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(S.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-left", size=18),
                on_click=S.prev_page,
                opacity=rx.cond(S.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(S.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-right", size=18),
                on_click=S.next_page,
                opacity=rx.cond(S.page_number == S.total_pages, 0.6, 1),
                color_scheme=rx.cond(S.page_number == S.total_pages, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevrons-right", size=18),
                on_click=S.last_page,
                opacity=rx.cond(S.page_number == S.total_pages, 0.6, 1),
                color_scheme=rx.cond(S.page_number == S.total_pages, "gray", "accent"),
                variant="soft",
            ),
            spacing="2",
            align="center",
            justify="end",
        ),
        spacing="5",
        margin_top="1em",
        width="100%",
        justify="end",
    )

# ─── berry table component ────────────────────────────────────────────
def berry_table() -> rx.Component:
    S = BerryTableState
    rows = S.current_page.to(list[BerryRow])

    return rx.box(
        # ── toolbar ────────────────────────────────────────────────
        rx.flex(
            # sort controls
            rx.flex(
                rx.cond(
                    S.sort_reverse,
                    rx.icon("arrow-down-z-a", size=28, cursor="pointer", on_click=S.toggle_sort),
                    rx.icon("arrow-down-a-z", size=28, cursor="pointer", on_click=S.toggle_sort),
                ),
                rx.select(
                    ["bunch_id", "berry_id", "berry_size"],
                    placeholder="Sort by…",
                    size="3",
                    on_change=S.set_sort_value,
                ),
                spacing="3",
                align="center",
            ),
            # export button
            rx.button(
                rx.icon("arrow-down-to-line", size=20),
                "Export",
                size="3",
                variant="surface",
                display=["none", "none", "none", "flex"],
                on_click=rx.download(url="/data/berry_data.csv"),
            ),
            spacing="3",
            align="center",
            justify="between",
            width="100%",
            padding_bottom="1em",
        ),

        # ── table ────────────────────────────────────────────────
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _berry_header_cell("Bunch ID", "hash"),
                    _berry_header_cell("Berry ID", "hash"),
                    _berry_header_cell("Size", "ruler"),
                )
            ),
            rx.table.body(
                rx.foreach(rows, lambda r, i: _show_berry_row(r, i))
            ),
            variant="surface",
            size="3",
            width="100%",
        ),

        # ── pagination footer ────────────────────────────────────
        _berry_pagination_view(),

        width="100%",
    )
