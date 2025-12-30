# widgets/request_history.py
from datetime import datetime
import os
import pickle
from typing import List
from httpx import Response
from widgets.history_item import HistoryItemWidget
from textual.app import ComposeResult
from textual.widgets import Static, ListView, Label


class HistoryItem:
    def __init__(
        self,
        method: str,
        url: str,
        status: int,
        timestamp: str,
        response: Response,
        elapsed: float
    ):
        self.method = method
        self.url = url
        self.status = status
        self.timestamp = timestamp
        self.response = response
        self.elapsed = elapsed


class RequestHistory(Static):
    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label("[b]History[/b]")
        yield ListView(id="history_list")

    def add_request(self, method: str, url: str, status: int, response: Response, elapsed: float):
        timestamp = datetime.now().strftime("%H:%M:%S")
        item = HistoryItemWidget(method, url, status, timestamp, response, elapsed)
        hi = HistoryItem(method, url, status, timestamp, response, elapsed)
        list_view = self.query_one("#history_list", ListView)
        list_view.insert(0, [item])
        file_path = f'./history/{timestamp.replace(":", "_")}.bin'
        with open(file_path, 'wb') as f:
            f.write(pickle.dumps(hi))

    def load_history(self):
        files = [f for f in os.listdir('./history') if f.endswith('.bin')]
        history_items: List[HistoryItem] = []
        for file_path in [f'./history/{file}' for file in files]:
            with open(file_path, 'rb') as f:
                history_item: HistoryItem = pickle.loads(f.read())
                history_items.append(history_item)

        history_items.sort(key=lambda item: item.timestamp, reverse=True)
        for i in history_items:
            item = HistoryItemWidget(i.method, i.url, i.status, i.timestamp, i.response, i.elapsed)
            list_view = self.query_one("#history_list", ListView)
            list_view.append(item)

        del history_items
