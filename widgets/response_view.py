# widgets/response_view.py
from contextlib import suppress
import json
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Static, TextArea, TabbedContent, TabPane

from services.request import parse_body, parse_headers, select_status_color



class ResponseView(Static):
    status = reactive(0)
    status_text = reactive("")
    headers = reactive({})
    body = reactive("")
    time_ms = reactive(0.0)

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Body", id="body_tab"):
                yield TextArea(id="response_body", read_only=True)
            
            with TabPane("Headers", id="headers_tab"):
                yield TextArea(id="response_headers", read_only=True)
            
            with TabPane("Info", id="info_tab"):
                yield Static(id="response_info")

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
