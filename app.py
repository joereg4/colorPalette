import os

import openai
from dotenv import load_dotenv
from flask import Flask

from routes import pages

load_dotenv()


def create_app():
    app = Flask(__name__)
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    app.register_blueprint(pages)
    return app


app = create_app()

# Entry point for ASGI servers
if __name__ == "__main__":
    import hypercorn.asyncio
    from hypercorn.config import Config
    import asyncio

    config = Config()
    config.bind = ["0.0.0.0:8000"]  # You can change the port if needed
    asyncio.run(hypercorn.asyncio.serve(app, config))
