# widgets/request_editor.py
from typing import Optional
from textual import on
from textual.containers import Horizontal
from textual.app import ComposeResult
from textual.reactive import reactive as ref
from textual.containers import Container, Horizontal
from textual.widgets import (
    Button, Input, Select,
    TextArea, TabbedContent, TabPane
)


METHODS = ('GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS')


class RequestEditor(Container):

    method = ref[str]("POST")
    url = ref[str]("https://httpbin.org/post")
    headers_text = ref[Optional[str]](None)
    body_text = ref[Optional[str]](None)

    def compose(self) -> ComposeResult:
        with Horizontal(classes="request-line"):
            yield Select(
                id="method",
                value="POST",
                options=[(i, i) for i in METHODS],
                classes="method-select"
            )
            yield Input(
                id="url",
                placeholder="https://httpbin.org/post",
                classes="url-input",
                value="https://httpbin.org/post"
            )
            yield Button("Send", id="send", variant="primary")

        with TabbedContent():
            with TabPane("Body"):
                yield TextArea(id="request_body", language="json")
            with TabPane("Headers"):
                yield TextArea(id="request_headers", language="json")

    @on(Select.Changed, "#method")
    def select_changed(self, event: Select.Changed):
        self.method = str(event.value)

    @on(Input.Changed, "#url")
    def input_changed(self, event: Input.Changed):
        self.url = event.value

    @on(TextArea.Changed, "#request_body")
    def text_area_body_changed(self, event: TextArea.Changed):
        self.body_text = event.text_area.text

    @on(TextArea.Changed, "#request_headers")
    def text_area_headers_changed(self, event: TextArea.Changed):
        self.headers_text = event.text_area.text
