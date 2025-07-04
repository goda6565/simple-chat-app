from app.usecase.ports.output.llm.clint import LLMClient
from openai import OpenAI
from app.infrastructure.config import provide_config

class OpenAIClient(LLMClient):
    def __init__(self):
        config = provide_config()
        self.client = OpenAI(api_key=config.openai_api_key)

    def generate_response(self, question: str, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt + question}]
        )
        return response.choices[0].message.content or ""
    
def create_openai_client() -> OpenAIClient:
    return OpenAIClient()