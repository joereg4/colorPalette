import os
import openai
from flask import Flask
from routes import pages
from dotenv import load_dotenv

load_dotenv()


# config = dotenv_values('.env');
# openai.api_key = config["OPENAI_API_KEY"]

def create_app():
    app = Flask(__name__)
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    app.register_blueprint(pages)
    return app
