from app.infrastructure.fastapi.application import create_fastapi_application
from app.infrastructure.fastapi.handler.stream.chat_stream import create_chat_stream_handler
from app.infrastructure.fastapi.handler.ui.ui import create_ui_handler
from app.usecase.stream.chat_session import create_chat_session_usecase

from app.infrastructure.memory.repository.chat import create_chat_repository
from app.infrastructure.openai.client import create_openai_client

llm_client = create_openai_client()
chat_repository = create_chat_repository()
chat_session_usecase = create_chat_session_usecase(llm_client, chat_repository)
stream_handler = create_chat_stream_handler(chat_session_usecase)
ui_handler = create_ui_handler()
fastapi_application = create_fastapi_application(stream_handler, ui_handler)
app = fastapi_application.application()