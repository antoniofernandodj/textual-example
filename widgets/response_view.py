# widgets/response_view.py
from contextlib import suppress
from httpx import Response
from textual import on
from textual.app import ComposeResult
from textual.reactive import reactive as ref
from textual.widgets import Static, TextArea, TabbedContent, TabPane, Button, Label
from services.logging import setup_logging
from services.request import parse_body, parse_headers, select_status_color
from widgets.request_history import RequestHistory


logger = setup_logging(__name__)


class ResponseView(Static):
    status = ref(0)
    status_text = ref("")
    headers = ref({})
    body = ref("")
    time_ms = ref(0.0)

    def __init__(self, h: RequestHistory):
        super().__init__()
        self.request_history = h

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Body", id="body_tab"):
                yield TextArea(id="response_body", read_only=True)
            
            with TabPane("Headers", id="headers_tab"):
                yield TextArea(id="response_headers", read_only=True)
            
            with TabPane("Info", id="info_tab"):
                yield Static(id="response_info")

            with TabPane("Delete", id="delete_tab"):
                yield Label('Tem Certeza que deseja remover esta response?', classes='delete_confirm')
                yield Button('Remove', id="delete_button")

    @on(Button.Pressed, '#delete_button')
    def delete_response(self, event: Button.Pressed):
        self.request_history.remove_response()

    def watch_status(self, status: int):
        self._update_display()

    def watch_body(self, body: str):
        self._update_display()

    def watch_headers(self, headers: dict):
        self._update_display()

    def _update_display(self):
        with suppress(Exception):
            body_widget = self.query_one("#response_body", TextArea)
            headers_widget = self.query_one("#response_headers", TextArea)
            info_widget = self.query_one("#response_info", Static)

            body_widget.text = parse_body(self.body)
            headers_widget.text = parse_headers(self.headers)
            status_color = select_status_color(self.status)

            info_widget.update(
                f"[b]Status:[/b] [{status_color}]{self.status} {self.status_text}[/]\n"
                f"[b]Time:[/b] {self.time_ms}ms\n"
                f"[b]Size:[/b] {len(self.body)} bytes"
            )
