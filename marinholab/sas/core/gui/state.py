"""Helper for the dynamic `state` property used by the Qt style sheets in this package."""


def set_state(widget, state: str) -> None:
    """Set the `state` property and force Qt to re-evaluate the style sheet for the widget.

    `setProperty` alone does not restyle the widget; Qt's `unpolish`/`polish` pair (unrelated to
    the polisher station) is the standard way to refresh it. Does nothing if the state is unchanged.
    """
    if widget.property("state") == state:
        return
    widget.setProperty("state", state)
    widget.style().unpolish(widget)
    widget.style().polish(widget)
