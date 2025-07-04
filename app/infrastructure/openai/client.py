from app.usecase.ports.output.llm.client import LLMClient
from openai import OpenAI
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from app.infrastructure.config import provide_config
from typing import Optional

SYSTEM_PROMPT = """
あなたは、ユーザーの質問に対して、適切な回答を生成するアシスタントです。
"""

class OpenAIClient(LLMClient):
    def __init__(self):
        config = provide_config()
        self.client = OpenAI(api_key=config.openai_api_key)

    def generate_response(self, question: str, prompt: str, chat_history: Optional[str]) -> str:
        messages: list[ChatCompletionMessageParam] = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # チャット履歴がある場合は、適切な形式でメッセージに追加
        if chat_history:
            messages.append({"role": "user", "content": self._parse_chat_history(chat_history)})
            
        messages.append({"role": "user", "content": prompt + question})
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages  # type: ignore
        )
        return response.choices[0].message.content or ""
    
    def _parse_chat_history(self, chat_history: str) -> str:
        print(chat_history)
        prompt = f"""
        過去の会話
        {chat_history}
        """
        return prompt

def create_openai_client() -> OpenAIClient:
    return OpenAIClient()