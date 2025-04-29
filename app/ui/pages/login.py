# app/ui/pages/login.py

import reflex as rx
from app.ui.state.auth import AuthState

@rx.page(route="/", title="Login")
def login_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                # ── Logo & title ─────────────────────────────
                rx.center(
                    rx.image(
                        src="/logo.jpg",
                        width="2.5em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Sign in to your account",
                        size="6",
                        as_="h2",
                        text_align="center",
                        width="100%",
                    ),
                    direction="column",
                    spacing="5",
                    width="100%",
                ),

                # ── Username field ───────────────────────────
                rx.vstack(
                    rx.text(
                        "Username",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("user")),
                        placeholder="your username",
                        size="3",
                        width="100%",
                        on_blur=AuthState.set_username,
                    ),
                    spacing="2",
                    width="100%",
                ),

                # ── Password field ───────────────────────────
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "Password",
                            size="3",
                            weight="medium",
                        ),
                        rx.link(
                            "Forgot password?",
                            href="#",
                            size="3",
                        ),
                        justify="between",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("lock")),
                        placeholder="Enter your password",
                        type_="password",
                        size="3",
                        width="100%",
                        on_blur=AuthState.set_password,
                    ),
                    spacing="2",
                    width="100%",
                ),

                # ── Log in button ────────────────────────────
                rx.button(
                    "Sign in",
                    size="3",
                    width="100%",
                    on_click=AuthState.login,
                ),

                # ── Sign up prompt ───────────────────────────
                rx.center(
                    rx.text("New here?", size="3"),
                    rx.link("Sign up", href="/signup", size="3"),
                    opacity="0.8",
                    spacing="2",
                    direction="row",
                    width="100%",
                ),

                spacing="6",
                width="100%",
            ),
            max_width="28em",
            size="4",
            width="100%",
        ),
        height="100vh",
        align_items="center",
        justify_content="center",
    )
