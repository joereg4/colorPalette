from dotenv import load_dotenv
from flask import Flask

from routes import pages

# The OpenAI client in routes.py reads OPENAI_API_KEY from the environment,
# so the .env file must be loaded before any request is handled.
load_dotenv()


def create_app():
    app = Flask(__name__)

    # The only POST body this app accepts is a short form field; reject
    # anything larger before it reaches a handler (Werkzeug returns 413).
    app.config["MAX_CONTENT_LENGTH"] = 4096

    app.register_blueprint(pages)
    return app


app = create_app()


if __name__ == "__main__":
    import asyncio

    import hypercorn.asyncio
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:8000"]
    asyncio.run(hypercorn.asyncio.serve(app, config))
