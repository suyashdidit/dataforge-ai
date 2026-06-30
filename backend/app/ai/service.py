from app.ai.openai_provider import OpenAIProvider
from app.ai.prompts import SQL_EXPLAIN_PROMPT


class AIService:

    def __init__(self):
        self.provider = OpenAIProvider()

    def explain_sql(self, sql: str):

        prompt = SQL_EXPLAIN_PROMPT.format(sql=sql)

        return self.provider.generate(prompt)