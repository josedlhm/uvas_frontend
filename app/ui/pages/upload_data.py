# app/ui/pages/upload_data.py

import reflex as rx
from app.ui.layouts.shell import template
from app.ui.state.upload_data import UploadDataState
from app.ui.components.upload_data_table import upload_data_table

@template(
    route="/uploads",
    title="Uploaded Data",
    on_load=[UploadDataState.load_upload_data],
)
def upload_data_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Uploaded Data", size="5", align="left", margin_bottom="1em"),
        upload_data_table(),
        spacing="2",
        width="100%",
    )
