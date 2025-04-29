# app/ui/components/upload_data_table.py

import reflex as rx
from app.ui.state.upload_data import UploadDataState, UploadDataRow

def _upload_header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(rx.icon(icon, size=18), rx.text(text), spacing="2", align="center")
    )

def _upload_row(row: UploadDataRow, idx: int) -> rx.Component:
    bg    = rx.cond(idx % 2 == 0, rx.color("gray", 1), rx.color("accent", 2))
    hover = rx.cond(idx % 2 == 0, rx.color("gray", 3), rx.color("accent", 3))
    return rx.table.row(
        rx.table.row_header_cell(row.crop_type),
        rx.table.cell(row.variety),
        rx.table.cell(row.location),
        rx.table.cell(row.day),
        rx.table.cell(row.hour),
        style={"_hover": {"bg": hover}, "bg": bg},
        align="center",
    )

def upload_data_table() -> rx.Component:
    S = UploadDataState
    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _upload_header_cell("Crop Type", "flower"),
                    _upload_header_cell("Variety",    "leaf"),
                    _upload_header_cell("Location",   "map-pin"),
                    _upload_header_cell("Day",        "calendar"),
                    _upload_header_cell("Hour",       "clock"),
                )
            ),
            rx.table.body(
                rx.foreach(S.rows, lambda r, i: _upload_row(r, i))
            ),
            variant="surface",
            size="3",
            width="100%",
        ),
        width="100%",
    )
