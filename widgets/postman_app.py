# widgets/postman_app.py
from typing import cast
import httpx
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, ListView, TextArea, TabbedContent, TabPane
from textual.containers import Horizontal, Vertical
from textual.binding import Binding
from services.request import RequestError, make_request
from widgets.history_item import HistoryItemWidget
from widgets.request_editor import RequestEditor
from widgets.request_history import RequestHistory
from widgets.response_view import ResponseView


class PostmanApp(App):

    BINDINGS = [
        Binding("ctrl+s", "send_request", "Send Request"),
        Binding("ctrl+q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.history.load_history()
        url_widget = self.query_one("#url")
        url_widget.focus()

    def compose(self) -> ComposeResult:
            yield Header()
            with Horizontal():
                with Vertical(id="sidebar"):
                    self.history = RequestHistory()
                    yield self.history

                with Vertical(id="main"):
                    with TabbedContent(id="main_tabs"):
                        with TabPane("REQUEST", id="pane_request"):
                            self.editor = RequestEditor()
                            yield self.editor
                        with TabPane("RESPONSE", id="pane_response"):
                            self.response_view = ResponseView()
                            yield self.response_view
            yield Footer()

    async def on_button_pressed(self, event: Button.Pressed):
        try:
            if event.button.id == "send":
                await self.action_send_request()
        except Exception as e:
            self.handle_exception(e)

    async def on_list_view_selected(self, event: ListView.Selected):
        history_item = cast(HistoryItemWidget, event.item)
        self.set_response_data(
            status=history_item.status,
            status_text=history_item.response.reason_phrase,
            headers=dict(history_item.response.headers),
            body=history_item.response.text,
            time_ms=float(history_item.elapsed)
        )


    async def action_send_request(self):
        body_text_widget = self.editor.query_one("#request_body", TextArea)
        headers_text_widget = self.editor.query_one("#request_headers", TextArea)

        response, elapsed = await make_request(
            url=str(self.editor.url),
            method=str(self.editor.method),
            body_text=body_text_widget.text,
            headers_text=headers_text_widget.text
        )

        self.set_response_data(
            status=response.status_code,
            status_text=response.reason_phrase,
            headers=dict(response.headers),
            body=response.text,
            time_ms=int(elapsed)
        )

        self.history.add_request(
            method=str(response.request.method),
            url=str(response.request.url),
            status=int(response.status_code),
            response=response,
            elapsed=elapsed
        )

        self.notify(
            message=f"Requisição finalizada: {response.status_code}",
            severity="information"
        )

        self.screen.set_focus(None)

        main_tabs = self.query_one("#main_tabs", TabbedContent)
        main_tabs.active = "pane_response"


    def handle_exception(self, error: Exception) -> None:
        traceback_obj = error.__traceback__
        if isinstance(error, RequestError):
            self.notify(error.message, severity="error")
            return

        if isinstance(error, httpx.TimeoutException):
            self.notify("Timeout na requisição", severity="error")
            self.response_view.body = "A requisição expirou após 30 segundos."
            return

        if isinstance(error, httpx.RequestError):
            self.notify(f"Erro de rede: {error}", severity="error")
            self.response_view.body = f"Erro: {error}"
            return

        self.notify("Erro interno inesperado, ver o log.", severity="error")

        with open("error.log", "a") as f:
            import traceback
            f.write("".join(traceback.format_tb(traceback_obj)))
            f.write(f"{error}\n\n")

    def set_response_data(self, status, time_ms, status_text, headers, body):
        self.response_view.status = status
        self.response_view.time_ms = time_ms
        self.response_view.status_text = status_text
        self.response_view.headers = headers
        self.response_view.body = body
