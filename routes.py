import openai
from flask import Blueprint, render_template, request, url_for, current_app
import json

pages = Blueprint(
    "colors", __name__, template_folder="templates", static_folder="static"
)


def get_colors(msg):
    messages = [
        {"role": "system",
         "content": "You are a color palette generating assistant that responds to text prompts for color palettes.  You should generate color palettes that fit the theme, mood, or instructions in the prompt.  The palettes should be between 2 and 8 colors."},
        {"role": "user",
         "content": "Convert the following verbal description of a color palette into a list of colors: The Mediterranean Sea"},
        {"role": "assistant", "content": '["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]'},
        {"role": "user",
         "content": "Convert the following verbal description of a color palette into a list of colors: sage, nature, earth"},
        {"role": "assistant", "content": '["#EDF1D6", "#9DC08B", "#609966", "#40513B"]'},
        {"role": "user",
         "content": f"Convert the following verbal description of a color palette into a list of colors: {msg}"},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=200,
    )

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
