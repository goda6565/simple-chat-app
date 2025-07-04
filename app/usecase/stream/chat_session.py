import uuid
from datetime import datetime

from app.usecase.ports.input.stream.chat_session import ChatSessionInputPort, ChatSessionInput, ChatSessionOutput, StepOutput
from app.usecase.ports.output.llm.clint import LLMClient
from app.domain.chat.repository.chat import ChatRepository
from app.domain.chat.entity.chat import create_chat, create_step
from app.domain.shared.value_object.id import create_id
from app.domain.shared.value_object.time import create_time
from app.domain.chat.value_object.title import create_title
from app.domain.chat.value_object.question import create_question
from app.domain.chat.value_object.answer import create_answer

GENERATE_TITLE_PROMPT = """
以下の質問に対して、適切なタイトルを生成してください。（チャットのタイトルになります。）
"""

GENERATE_STEP_PROMPT = """
以下の質問に対して、適切な回答を生成してください。
"""

class ChatSessionUseCase(ChatSessionInputPort):
    def __init__(self, llm_client: LLMClient, chat_repository: ChatRepository):
        self.llm_client = llm_client
        self.chat_repository = chat_repository

    def execute(self, input: ChatSessionInput) -> ChatSessionOutput:
        try:
            # 新規初回ループの場合
            if input.is_first and input.title is None and input.created_at is None and input.updated_at is None:
                # タイトルを生成
                title = self.llm_client.generate_response(input.current_question, GENERATE_TITLE_PROMPT)
                # チャット値オブジェクトを作成
                chat_id = create_id(str(uuid.uuid4()))
                title = create_title(title)
                steps = []
                created_at = create_time(datetime.now())
                updated_at = create_time(datetime.now())
                # チャットエンティティを作成
                chat = create_chat(chat_id, title, steps, created_at, updated_at)
                # チャットを保存
                self.chat_repository.create(chat)

            # 再開初回ループの場合
            elif input.is_first and input.title is not None and input.created_at is not None and input.updated_at is not None:
                # チャットIDを作成
                chat_id = create_id(input.chat_id)
                # チャットを取得
                chat = self.chat_repository.find_by_id(chat_id)
                # チャットが存在しない場合はエラー
                if chat is None:
                    raise Exception(f"Chat with id {input.chat_id} not found")

            # ループの途中の場合
            elif not input.is_first and input.title is not None and input.created_at is not None and input.updated_at is not None:
                # チャットを再構成
                chat_id = create_id(input.chat_id)
                title = create_title(input.title)
                steps = []
                created_at = create_time(input.created_at)
                updated_at = create_time(input.updated_at)
                chat = create_chat(chat_id, title, steps, created_at, updated_at)
                # ステップを作成
                for step in input.steps:
                    id = create_id(step.id)
                    question = create_question(step.question)
                    answer = create_answer(step.answer)
                    created_at = create_time(step.created_at)
                    step = create_step(id, chat_id, question, answer, created_at)
                    chat.add_step(step)
        
            # 回答を生成
            answer_raw = self.llm_client.generate_response(input.current_question, GENERATE_STEP_PROMPT)
            # ステップを作成
            id = create_id(str(uuid.uuid4()))
            question = create_question(input.current_question)
            answer = create_answer(answer_raw)
            created_at = create_time(datetime.now())

            # 新しいステップを作成
            step = create_step(id, chat_id, question, answer, created_at)
            chat.add_step(step)
            # チャットを更新
            self.chat_repository.update(chat)

            output_steps: list[StepOutput] = []
            for step in chat.get_steps():
                output_steps.append(StepOutput(step.get_id().value(), step.get_question().value(), step.get_answer().value(), step.get_created_at().value()))

            return ChatSessionOutput(chat_id.value(), answer_raw, chat.get_title().value(), output_steps, chat.get_created_at().value(), chat.get_updated_at().value())

        except Exception as e:
            raise Exception(f"Error generating response: {e}")
        
def create_chat_session_usecase(llm_client: LLMClient, chat_repository: ChatRepository) -> ChatSessionUseCase:
    return ChatSessionUseCase(llm_client, chat_repository)