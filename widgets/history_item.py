# widgets/history_item.py
from httpx import Response
from textual.app import ComposeResult
from textual.widgets import Static, ListItem


class HistoryItemWidget(ListItem):
    def __init__(
        self,
        method: str,
        url: str,
        status: int,
        timestamp: str,
        response: Response,
        elapsed: float,
    ):
        super().__init__()
        self.timestamp = timestamp
        self.method = method
        self.url = url
        self.status = status
        self.response = response
        self.elapsed = elapsed

    def compose(self) -> ComposeResult:
        status_color = (
            "green" if 200 <= self.status < 300
            else "red" if self.status >= 400 else "yellow"
        )

        yield Static(
            f"[b]{self.method}[/b] [{status_color}]{self.status}[/] {self.url[:40]}..."
            f"\n[dim]{self.timestamp}[/]"
        )
