from fastapi import FastAPI
import uvicorn

from app.infrastructure.fastapi.handler.stream.chat_stream import ChatStreamHandler
from app.infrastructure.fastapi.handler.ui.ui import UIHandler

class FastAPIServer:
    def __init__(self, stream_handler: ChatStreamHandler, ui_handler: UIHandler):
        self.app = FastAPI()
        self.stream_handler = stream_handler
        self.ui_handler = ui_handler

        # ルーティングを登録
        self.app.add_websocket_route("/chat/stream", self.stream_handler.handle)
        self.app.add_api_route("/", self.ui_handler.handle, methods=["GET"])

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """アプリケーションを起動する。

        FastAPI インスタンス自体には run メソッドが無いため、
        uvicorn でサーバーを立ち上げる。
        """

        uvicorn.run(self.app, host=host, port=port)