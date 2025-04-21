import reflex as rx

class BreadcrumbState(rx.State):
    """Computes a dynamic breadcrumb string from the current route."""

    @rx.var
    def breadcrumb(self) -> str:
        # Get the current route (e.g., "/plant" or "/fruit/")
        path = self.router.page.path
        
        # Remove trailing slash if present
        if path.endswith("/"):
            path = path[:-1]
        
        # Remove the leading slash if present
        if path.startswith("/"):
            path = path[1:]
        
        # If there's no path, default to "Home"
        if not path:
            return "Home"
        
        # Split the path into segments (e.g., ["plant"] or ["scans", "plant"])
        segments = [segment.capitalize() for segment in path.split("/") if segment]
        
        # Check: if there's exactly one segment and it is "Plant" or "Fruit",
        # then assume the parent category is "Scans"
        if len(segments) == 1 and segments[0] in ["Plant", "Fruit"]:
            return f"Scans > {segments[0]}"
        else:
            # Otherwise, join all segments with a separator.
            return " > ".join(segments)
