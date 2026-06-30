from app.ai.base import LLMProvider


class OpenAIProvider(LLMProvider):

    def generate(self, prompt: str) -> str:
        return "OpenAI response placeholder"