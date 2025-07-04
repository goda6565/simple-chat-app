from app.infrastructure.fastapi.server import FastAPIServer
from app.infrastructure.fastapi.handler.stream.chat_stream import ChatStreamHandler
from app.infrastructure.fastapi.handler.ui.ui import UIHandler
from app.usecase.stream.chat_session import create_chat_session_usecase

from app.infrastructure.memory.repository.chat import create_chat_repository
from app.infrastructure.openai.client import create_openai_client

def main():
    llm_client = create_openai_client()
    chat_repository = create_chat_repository()
    chat_session_usecase = create_chat_session_usecase(llm_client, chat_repository)
    stream_handler = ChatStreamHandler(chat_session_usecase)
    ui_handler = UIHandler()
    server = FastAPIServer(stream_handler, ui_handler)
    server.run()


if __name__ == "__main__":
    main()
