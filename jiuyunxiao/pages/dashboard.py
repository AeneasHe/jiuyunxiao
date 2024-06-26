# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""The dashboard page."""
from jiuyunxiao.templates import template

import nextpy as xt


@template(route="/dashboard", title="看板")
def dashboard() -> xt.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return xt.vstack(
        xt.heading("Dashboard", font_size="3em"),
        xt.text("Welcome to Nextpy!"),
        xt.text(
            "You can edit this page in ",
            xt.code("{your_app}/pages/dashboard.py"),
        ),
    )
