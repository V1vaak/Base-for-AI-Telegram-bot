import os

from openai import AsyncOpenAI

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


async def ai_generate(text: str):
  client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv('AI_TOKEN'),
  )

  completion = await client.chat.completions.create(
    model="deepseek/deepseek-chat-v3-0324",
    messages=[
      {
        "role": "user",
        "content": text
      }
    ]
  )
  return completion.choices[0].message.content