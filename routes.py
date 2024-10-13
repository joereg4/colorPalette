import json
from typing import List

import openai
from flask import Blueprint, render_template, request
import asyncio

CHAT_MODEL = "gpt-4o"

pages = Blueprint(
    "colors", __name__, template_folder="templates", static_folder="static"
)

# Extract messages to global constant for better readability and a slight performance tweak.
DEFAULT_MESSAGES = [
    {"role": "system",
     "content": "You are a color palette generating assistant that responds to text prompts for color palettes. You "
                "should generate color palettes that fit the theme, mood, or instructions in the prompt. The palettes "
                "should be between 2 and 8 colors."},
    {"role": "user",
     "content": "Convert the following verbal description of a color palette into a list of colors: The Mediterranean "
                "Sea"},
    {"role": "assistant", "content": '["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]'},
    {"role": "user",
     "content": "Convert the following verbal description of a color palette into a list of colors: sage, nature, earth"},
    {"role": "assistant", "content": '["#EDF1D6", "#9DC08B", "#609966", "#40513B"]'},
    # Last message is created on-the-fly based on function's argument.
]


async def get_colors(msg: str) -> List[str]:
    """
    Asynchronous function to get color codes based on the message using OpenAI service.
    It uses gpt-4o model for this purpose.
    """
    messages = DEFAULT_MESSAGES + [
        {"role": "user",
         "content": f"Convert the following verbal description of a color palette into a "
                    f"list of colors: {msg}"}
    ]

    def fetch_colors():
        response = openai.ChatCompletion.create(
            model=CHAT_MODEL,
            messages=messages,
            max_tokens=200,
        )
        return response

    response = await asyncio.to_thread(fetch_colors)

    colors = json.loads(response["choices"][0]["message"]["content"])
    return colors


@pages.route("/palette", methods=["POST"])
async def prompt_to_palette():
    query = request.form.get("query")
    if not query:
        return {"error": "No query provided."}, 400
    try:
        colors = await get_colors(query)
        return {"colors": colors}
    except Exception as e:
        return {"error": str(e)}, 500


@pages.route("/")
def index():
    return render_template("index.html")
