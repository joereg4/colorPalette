import openai
from flask import Blueprint, render_template, request, url_for, current_app
import json
from typing import List

CHAT_MODEL = 'gpt-4o-2024-08-06'

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


def get_colors(msg: str) -> List[str]:
    """
    Function to get color codes based on the message using OpenAI service.
    It uses gpt-4o model for this purpose.
    """
    messages = DEFAULT_MESSAGES + [{"role": "user",
                                    "content": f"Convert the following verbal description of a color palette into a "
                                               f"list of colors: {msg}"}]
    response = openai.ChatCompletion.create(
        model=CHAT_MODEL,
        messages=messages,
        max_tokens=200,
    )
    # It's assumed that response is always valid and contains required fields.
    colors = json.loads(response["choices"][0]["message"]["content"])
    return colors


@pages.route("/palette", methods=["POST"])
def prompt_to_palette():
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}


@pages.route("/")
def index():
    return render_template("index.html")
