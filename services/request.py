
from datetime import datetime
import json
from time import perf_counter

import httpx


class RequestError(Exception):


    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


async def make_request(url: str, method: str, body_text: str, headers_text: str):
    if not url:
        raise RequestError("URL é obrigatória")

    headers = {}
    if headers_text.strip():
        try:
            headers = json.loads(headers_text)
        except json.JSONDecodeError:
            raise RequestError("JSON de Headers inválido")

    body = None
    if body_text.strip():
        try:
            body = json.loads(body_text)
        except json.JSONDecodeError:
            body = body_text

    start = perf_counter()

    async with httpx.AsyncClient(timeout=30) as client:
        if isinstance(body, dict):
            response = await client.request(method, url, json=body, headers=headers)
        elif body:
            response = await client.request(method, url, content=body, headers=headers)
        else:
            response = await client.request(method, url, headers=headers)

    elapsed = (perf_counter() - start) * 1000

    return response, elapsed

def parse_body(body):
    if not body:
        return ""

    try:
        return json.dumps(
            json.loads(body),
            indent=2,
            ensure_ascii=False
        )
    except Exception:
        return body


def parse_headers(h):
    return json.dumps(dict(h), indent=2, ensure_ascii=False)


def select_status_color(status):
    if status >= 200 and status < 300:
        status_color = "green"
    elif status >= 400:
        status_color = "red"
    else:
        status_color = "yellow"
    
    return status_color
