import reflex as rx
from app.ui.state.breadcrumb import BreadcrumbState  

def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium"),
        href=url,
    )

def navbar() -> rx.Component:
    return rx.box(
        # Desktop layout: three columns using flex.
        rx.desktop_only(
            rx.flex(
                # Left Column: Logo + Brand
                rx.box(
                    rx.hstack(
                        rx.image(
                            src="/logo.jpg",
                            width="2.25em",
                            height="auto",
                            border_radius="25%",
                        ),
                        rx.heading("Macanudo", size="7", weight="bold"),
                    ),
                    width="33%",
                    display="flex",
                    align_items="center",
                    justify_content="flex-start",
                ),
                # Center Column: Dynamic Breadcrumb / Current Page Title
                rx.box(
                    rx.heading(
                        BreadcrumbState.breadcrumb,  # dynamic reactive breadcrumb
                        size="6",
                        text_align="center",
                    ),
                    width="34%",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                # Right Column: Placeholder for additional content (e.g. a link)
                rx.box(
                    rx.hstack(
                        navbar_link("Contact", "/#"),
                    ),
                    width="33%",
                    display="flex",
                    align_items="center",
                    justify_content="flex-end",
                ),
                width="100%",
                padding="1em",
                background_color=rx.color("accent", 3),
                box_shadow="0 1px 3px rgba(0,0,0,0.1)",
            )
        ),
        # Mobile and tablet layout remains as previously defined
        rx.mobile_and_tablet(
            rx.flex(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading("Macanudo", size="6", weight="bold"),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon("menu", size=30)
                    ),
                    rx.menu.content(
                        rx.menu.item("Home"),
                        rx.menu.item("About"),
                        rx.menu.item("Pricing"),
                        rx.menu.item("Contact"),
                    ),
                    justify="end",
                ),
                width="100%",
                padding="1em",
                background_color=rx.color("accent", 3),
            )
        ),
        width="100%",
    )
