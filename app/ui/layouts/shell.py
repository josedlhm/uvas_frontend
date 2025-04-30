from __future__ import annotations
import reflex as rx

from typing import Callable
from app.ui.components.navbar import navbar
from app.ui.components.sidebar import sidebar_bottom_profile
from .. import styles

class ThemeState(rx.State):
    """The state for the theme of the app."""

    accent_color: str = "gray"

    gray_color: str = "crimson"

    radius: str = "large"

    scaling: str = "100%"

def template(
    route: str,
    title: str,
    on_load: rx.EventHandler | list[rx.EventHandler] | None = None,
) -> Callable[[Callable[[], rx.Component]], rx.Component]:
    
    
    
    """Decorator to wrap a page in navbar/sidebar + Theme + @rx.page."""
    def decorator(page_fn: Callable[[], rx.Component]) -> rx.Component:
        def templated_page():
            return rx.flex(
                    navbar(),                    
                    rx.hstack(                   
                        sidebar_bottom_profile(),
                        rx.box(                  
                            page_fn(),
                            padding = '1.5rem',
                            w="100%",
                            flex="1",
  
                            min_h = "0"
                        ),
                        w="100%",
                        min_h = "0",
                        flex = "1", 
                        align_items="stretch"
                    ),
                    spacing="0",
                    w="100%",
                    align_items="stretch",
                    height = "100vh",
                    direction = "column"
                
            )
        
            
        @rx.page(
        route=route,
        title=title,
        on_load=on_load,
        )

            # 2) wrap it in rx.theme so RadixThemesCard gets imported
        def theme_wrap():
            return rx.theme(
                templated_page(),
                has_background=True,
                accent_color=ThemeState.accent_color,
                gray_color=ThemeState.gray_color,
                radius=ThemeState.radius,
                scaling=ThemeState.scaling,
            )

        return theme_wrap
    return decorator