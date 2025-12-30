# widgets/request_editor.py
from textual.containers import Horizontal
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.containers import Container, Horizontal
from textual.widgets import (
    Button, Input, Select,
    TextArea, TabbedContent, TabPane
)


METHODS = ('GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS')


class RequestEditor(Container):

    def __init__(self):
        super().__init__()
        self.method = reactive("POST")
        self.url = reactive("https://httpbin.org/post")
        self.headers_text = reactive("")
        self.body_text = reactive("")


    def compose(self) -> ComposeResult:
        with Horizontal(classes="request-line"):
            yield Select(
                options=[(i, i) for i in METHODS],
                value="POST",
                id="method",
                classes="method-select"
            )
            yield Input(
                placeholder="https://httpbin.org/post",
                id="url",
                classes="url-input",
                value="https://httpbin.org/post"
            )
            yield Button("Send", id="send", variant="primary")

        with TabbedContent():
            with TabPane("Body"):
                yield TextArea(id="request_body", language="json")
            with TabPane("Headers"):
                yield TextArea(id="request_headers", language="json")

    def on_select_changed(self, event: Select.Changed):
        if event.select.id == "method":
            self.method = event.value

    def on_input_changed(self, event: Input.Changed):
        if event.input.id == "url":
            self.url = event.value

    def on_text_area_changed(self, event: TextArea.Changed):
        if event.text_area.id == "request_body":
            self.body_text = event.text_area.text

        elif event.text_area.id == "request_headers":
            self.headers_text = event.text_area.text
