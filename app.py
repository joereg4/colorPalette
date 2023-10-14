import os
import openai
from flask import Flask
from routes import pages
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    app.register_blueprint(pages)
    return app
