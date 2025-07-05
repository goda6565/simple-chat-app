from fastapi import WebSocket
from app.usecase.ports.input.stream.chat_session import ChatSessionInputPort, ChatSessionInput, StepInput

# path: /chat/stream
# params:
# json:
# chat_id: str
# current_question: str
# output:
# answer: str

class ChatStreamHandler:
    """WebSocket ストリーム用ハンドラ。

    WebSocket インスタンスはハンドラ呼び出し時に受け取り、
    UseCase などの依存はコンストラクタで注入する。
    """

    def __init__(self, chat_session_usecase: ChatSessionInputPort):
        self.chat_session_usecase = chat_session_usecase

    async def handle(self, websocket: WebSocket):
        await websocket.accept()
        is_first = True
        title = None
        steps = []
        created_at = None
        updated_at = None

        while True:
            data = await websocket.receive_json()
            chat_id = data["chat_id"]
            current_question = data["current_question"]

            input = ChatSessionInput(
                chat_id=chat_id,
                is_first=is_first,
                title=title,
                current_question=current_question,
                steps=steps,
                created_at=created_at,
                updated_at=updated_at,
            )

            output = self.chat_session_usecase.execute(input)

            await websocket.send_text(output.answer)

            steps = [
                StepInput(step.id, step.question, step.answer, step.created_at)
                for step in output.steps
            ]
            is_first = False
            title = output.title
            created_at = output.created_at
            updated_at = output.updated_at