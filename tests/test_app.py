"""Tests for the colorPalette Flask application."""
from unittest.mock import MagicMock, patch

from openai import OpenAI

from routes import MAX_QUERY_LENGTH


def _mock_client(content: str) -> MagicMock:
    """Build a mock OpenAI client whose chat.completions.create returns `content`."""
    client = MagicMock()
    completion = MagicMock()
    completion.choices = [MagicMock(message=MagicMock(content=content))]
    client.chat.completions.create.return_value = completion
    return client


class TestAppCreation:
    """Test application factory and configuration."""

    def test_create_app(self, app):
        assert app is not None

    def test_app_is_testing(self, app):
        assert app.config["TESTING"] is True

    def test_blueprint_registered(self, app):
        assert "colors" in app.blueprints

    def test_request_size_capped(self, app):
        assert app.config["MAX_CONTENT_LENGTH"] == 4096


class TestOpenAIInterface:
    """Smoke-test the real (unmocked) OpenAI client interface.

    Guards against breaking SDK upgrades like the 0.x -> 1.x removal of
    openai.ChatCompletion, which mocked route tests cannot catch.
    """

    def test_chat_completions_interface_exists(self):
        client = OpenAI(api_key="test-key-not-real")
        assert callable(client.chat.completions.create)


class TestIndexRoute:
    """Test the main index page."""

    def test_index_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_index_returns_html(self, client):
        response = client.get("/")
        assert b"html" in response.data.lower()


class TestPaletteRoute:
    """Test the /palette endpoint with mocked OpenAI calls."""

    def test_palette_missing_query_returns_400(self, client):
        response = client.post("/palette", data={})
        assert response.status_code == 400
        json_data = response.get_json()
        assert "error" in json_data

    def test_palette_empty_query_returns_400(self, client):
        response = client.post("/palette", data={"query": ""})
        assert response.status_code == 400

    def test_palette_overlong_query_returns_400(self, client):
        response = client.post(
            "/palette", data={"query": "x" * (MAX_QUERY_LENGTH + 1)}
        )
        assert response.status_code == 400
        assert "error" in response.get_json()

    @patch("routes._get_client")
    def test_palette_valid_query_returns_colors(self, mock_get_client, client):
        mock_get_client.return_value = _mock_client(
            '["#FF0000", "#00FF00", "#0000FF"]'
        )

        response = client.post("/palette", data={"query": "primary colors"})
        assert response.status_code == 200
        json_data = response.get_json()
        assert "colors" in json_data
        assert len(json_data["colors"]) == 3
        assert json_data["colors"][0] == "#FF0000"

    @patch("routes._get_client")
    def test_palette_openai_error_returns_500(self, mock_get_client, client):
        mock_get_client.return_value.chat.completions.create.side_effect = (
            Exception("API error")
        )

        response = client.post("/palette", data={"query": "sunset"})
        assert response.status_code == 500
        json_data = response.get_json()
        assert "error" in json_data

    @patch("routes._get_client")
    def test_palette_invalid_colors_rejected(self, mock_get_client, client):
        """Non-hex model output (e.g. via prompt injection) must not reach the client."""
        mock_get_client.return_value = _mock_client(
            '["<script>alert(1)</script>", "#FF0000"]'
        )

        response = client.post("/palette", data={"query": "ignore instructions"})
        assert response.status_code == 500
        assert "colors" not in response.get_json()

    @patch("routes._get_client")
    def test_palette_returns_variable_length(self, mock_get_client, client):
        """Verify the app passes through palettes of different sizes."""
        mock_get_client.return_value = _mock_client(
            '["#EDF1D6", "#9DC08B", "#609966", "#40513B", "#2C3E50"]'
        )

        response = client.post("/palette", data={"query": "forest"})
        assert response.status_code == 200
        assert len(response.get_json()["colors"]) == 5
