from pydantic import BaseModel
from shiny.express import input, render, ui
from shiny_pydantic.render import render_ui


class ExampleModel(BaseModel):
    example_text: str = "Some default text"
    example_number: int = 5


with ui.sidebar():
    render_ui(ExampleModel)

with ui.card(full_screen=True):
    ui.card_header("Reactive Inputs")

    @render.text
    def reactive_text():
        return f"The current text value is: {input.example_text()}"

    @render.text
    def reactive_number():
        return f"The current numeric value is: {input.example_number()}"
