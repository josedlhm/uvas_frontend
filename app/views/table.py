# app/table_component.py
import reflex as rx
from app.table_state import BunchTableState, BunchRow

#  ─── header & row renderers ──────────────────────────────────────────
def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(rx.icon(icon, size=18), rx.text(text), spacing="2", align="center")
    )

def _show_row(row: BunchRow, index: int) -> rx.Component:
    bg    = rx.cond(index % 2 == 0, rx.color("gray", 1), rx.color("accent", 2))
    hover = rx.cond(index % 2 == 0, rx.color("gray", 3), rx.color("accent", 3))
    return rx.table.row(
        rx.table.row_header_cell(row.bunch_id),
        rx.table.cell(f"{row.n_visible_berries:,}"),
        rx.table.cell(f"{row.n_estimated_berries:,.1f}"),
        style={"_hover": {"bg": hover}, "bg": bg},
        align="center",
    )


#  ─── pagination footer ────────────────────────────────────────────────
def _pagination_view() -> rx.Component:
    S = BunchTableState
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

def bunch_table() -> rx.Component:
    S = BunchTableState
    typed_rows = S.current_page.to(list[BunchRow])

    return rx.box(
        # ─── toolbar ───────────────────────────────────────────────
        rx.flex(
            # ← inner flex containing only the sort controls
            rx.flex(
                rx.cond(
                    S.sort_reverse,
                    rx.icon("arrow-down-z-a", size=28, cursor="pointer", on_click=S.toggle_sort),
                    rx.icon("arrow-down-a-z", size=28, cursor="pointer", on_click=S.toggle_sort),
                ),
                rx.select(
                    ["bunch_id", "n_visible_berries", "n_estimated_berries"],
                    placeholder="Sort by…",
                    size="3",
                    on_change=S.set_sort_value,
                ),
                spacing="3",
                align="center",
            ),
            # ← second child: export button gets pushed to the right
            rx.button(
                rx.icon("arrow-down-to-line", size=20),
                "Export",
                size="3",
                variant="surface",
                display=["none", "none", "none", "flex"],
                on_click=rx.download(url="/data/new_data.csv"),
            ),
            spacing="3",
            align="center",
            justify="between",  # ← pushes child #1 to left, child #2 to right
            width="100%",
            padding_bottom="1em",
        ),

        # ─── the table ───────────────────────────────────────────────
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Bunch ID",           "hash"),
                    _header_cell("Visible Berries",    "eye"),
                    _header_cell("Estimated Berries",  "calculator"),
                )
            ),
            rx.table.body(
                rx.foreach(typed_rows, lambda r, i: _show_row(r, i))
            ),
            variant="surface",
            size="3",
            width="100%",
        ),

        # pagination footer…
        _pagination_view(),

        width="100%",
    )