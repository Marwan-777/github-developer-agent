from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv() 


client = OpenAI(
  api_key=os.getenv('openai_llm_key')
)

query = """
Hello :)
"""

def generate(messages, tools = None, model = "gpt-4o-mini"):
    completion = client.chat.completions.create(
    model=model,
    store=True,
    tools = tools,
    # tool_choice="auto",
    messages=messages
    )
    return completion.choices[0].message.content

def generate_stream(messages, tools = None, model = "gpt-4o-mini"):
    stream = client.chat.completions.create(
    model=model,
    store=True, 
    tools=tools,
    messages=messages,
    stream=True,
    )
    for chunk in  stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# for event in generate_stream(query):
#     print(event, end="", flush=True)