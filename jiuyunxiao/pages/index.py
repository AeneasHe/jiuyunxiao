# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""The home page of the app."""

from jiuyunxiao import styles
from jiuyunxiao.templates import template

import nextpy as xt


@template(route="/", title="首页", image="/github.svg")
def index() -> xt.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    return xt.vstack(
        xt.heading("九云霄命理馆", font_size="3em"),
        xt.text("欢迎来到九云霄命理馆"),
    )
