# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


def generate(prompt):
    client = genai.Client(
        api_key=os.getenv("gemini_key"),
    )

    model = "gemini-flash-latest"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""{prompt}"""),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch(
        )),
    ]
    generate_content_config = types.GenerateContentConfig(
        # thinkingConfig: {
        #     thinkingBudget: -1,
        # },
        tools=tools,
        system_instruction=[
            types.Part.from_text(text="""you are only a loan agent, your name is soma, you answer briefly, nicely and smart"""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")



while True:
    userinput = input("\nYou: ") 
    generate(userinput)





if __name__ == "__main__":
    generate()

