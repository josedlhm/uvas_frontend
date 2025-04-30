import reflex as rx


def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )

def sidebar_items() -> rx.Component:
    return rx.vstack(
        rx.heading("Scans", size="5", weight="bold", align="left", margin_bottom="0.5rem"),
        sidebar_item("Plant", "leaf", "/plant"),
        sidebar_item("Fruit", "apple", "/fruit"),
        sidebar_item("Uploads", "cloud-upload", "/uploads"),
        spacing="1",
        width="100%",
    )

def sidebar_bottom_profile() -> rx.Component:
    return rx.desktop_only(
        # this vstack is the ONE parent container
        rx.vstack(
            # 1) all your “Scans” links
            sidebar_items(),

            # 2) spacer that grows to fill the middle
            rx.spacer(),

            # 3) the bottom links + divider + profile
            rx.vstack(
                sidebar_item("Settings", "settings", "/#"),
                sidebar_item("Log out", "log-out", "/#"),
                spacing="1",
                width="100%",
            ),
            rx.divider(),
            rx.hstack(
                rx.icon_button(rx.icon("user"), size="3", radius="full"),
                rx.vstack(
                    rx.text("My account", size="3", weight="bold"),
                    rx.text("user@reflex.dev", size="2", weight="medium"),
                    spacing="0",
                    align="start",
                ),
                spacing="2",
                width="100%",
            ),

            # KEY PROPS on the container:
            height="100dvh",      # span the entire viewport
            width="16em",
            padding_x="1em",
            padding_y="1.5em",
            bg=rx.color("accent", 3),
            align="start",
            justify="between",    # push top group up, bottom group down
            flex=1,
            position="sticky",
            top="0px",
        ),
        # ── Mobile drawer ──
        rx.mobile_and_tablet(
            rx.drawer.root(
                rx.drawer.trigger(rx.icon("align-justify", size=30)),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.vstack(
                            rx.drawer.close(rx.icon("x", size=30)),
                            sidebar_items(),
                            rx.spacer(),
                            rx.vstack(
                                sidebar_item("Settings", "settings", "/#"),
                                sidebar_item("Log out", "log-out", "/#"),
                                spacing="1",
                            ),
                            rx.divider(margin="0"),
                            rx.hstack(
                                rx.icon_button(rx.icon("user"), size="3", radius="full"),
                                rx.vstack(
                                    rx.text("My account", size="3", weight="bold"),
                                    rx.text("user@reflex.dev", size="2", weight="medium"),
                                    spacing="0",
                                ),
                                spacing="2",
                            ),
                            spacing="5",
                        ),
                        width="20em",
                        padding="1.5em",
                        bg=rx.color("accent", 2),
                    )
                ),
                direction="left",
            ),
            padding="1em",
            
        ),
                direction="column",
        height="100%",      # fills available height
        width="16em",

    )
