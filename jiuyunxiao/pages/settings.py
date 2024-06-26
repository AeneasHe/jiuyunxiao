# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""The settings page."""

from jiuyunxiao.templates import template

import nextpy as xt


@template(route="/settings", title="设置")
def settings() -> xt.Component:
    """The settings page.

    Returns:
        The UI for the settings page.
    """
    return xt.vstack(
        xt.heading("Settings", font_size="3em"),
        xt.text("Welcome to Nextpy!"),
        xt.text(
            "You can edit this page in ",
            xt.code("{your_app}/pages/settings.py"),
        ),
    )
