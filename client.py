# GPT-3.5 Virtual Assistant

This code snippet demonstrates how to create a virtual assistant named Peter using OpenAI's GPT-3.5 model. Peter is designed to perform general tasks similar to Alexa and Google Assistant. The assistant can respond to user inputs based on provided prompts.

## Code Overview

- **API Initialization**: Initializes the OpenAI client with the provided API key.
- **Chat Completions**: Uses the `gpt-3.5-turbo` model to generate responses based on the given system and user messages.
- **Example Interaction**: The assistant responds to the query "What is coding?" with an explanation.

from openai import OpenAI

client = OpenAI(api_key="<your_openAI_api_key")
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Peter, skilled in general tasks like Alexa and Google."},
        {"role": "user", "content": "What is coding?"}
    ]
)

print(completion.choices[0].message['content'])
