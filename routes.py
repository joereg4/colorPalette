import asyncio
import json
import logging
import re
from typing import List

from flask import Blueprint, render_template, request
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

CHAT_MODEL = "gpt-4o"

# Cap prompt length so a single request can't run up token costs.
MAX_QUERY_LENGTH = 300

# Accept #RGB, #RGBA, #RRGGBB, and #RRGGBBAA hex color formats.
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{3,8}$")

pages = Blueprint(
    "colors", __name__, template_folder="templates", static_folder="static"
)

# Created lazily so the app can start (and tests can run) without an API key.
_client = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


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
        return _get_client().chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            max_tokens=200,
        )

    response = await asyncio.to_thread(fetch_colors)

    colors = json.loads(response.choices[0].message.content)

    # Defense-in-depth: only pass validated hex codes through to the client,
    # so prompt injection can't smuggle arbitrary strings into the response.
    if not isinstance(colors, list) or not colors or not all(
        isinstance(color, str) and HEX_COLOR_RE.match(color) for color in colors
    ):
        raise ValueError("Model returned an invalid color palette")

    return colors


@pages.route("/palette", methods=["POST"])
async def prompt_to_palette():
    query = request.form.get("query")
    if not query:
        return {"error": "No query provided."}, 400
    if len(query) > MAX_QUERY_LENGTH:
        return {"error": f"Query must be {MAX_QUERY_LENGTH} characters or fewer."}, 400
    try:
        colors = await get_colors(query)
        return {"colors": colors}
    except Exception as e:
        logger.error(f"Error generating palette: {str(e)}", exc_info=True)
        return {"error": "An error occurred while generating the color palette."}, 500


@pages.route("/")
def index():
    return render_template("index.html")
