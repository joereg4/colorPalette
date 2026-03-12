"""Tests for the colorPalette Flask application."""
from unittest.mock import patch, MagicMock

import pytest


class TestAppCreation:
    """Test application factory and configuration."""

    def test_create_app(self, app):
        assert app is not None

    def test_app_is_testing(self, app):
        assert app.config["TESTING"] is True

    def test_blueprint_registered(self, app):
        assert "colors" in app.blueprints


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

    @patch("routes.openai.ChatCompletion.create")
    def test_palette_valid_query_returns_colors(self, mock_create, client):
        mock_response = MagicMock()
        mock_response.__getitem__ = lambda self, key: {
            "choices": [
                {"message": {"content": '["#FF0000", "#00FF00", "#0000FF"]'}}
            ]
        }[key]
        mock_create.return_value = mock_response

        response = client.post("/palette", data={"query": "primary colors"})
        assert response.status_code == 200
        json_data = response.get_json()
        assert "colors" in json_data
        assert len(json_data["colors"]) == 3
        assert json_data["colors"][0] == "#FF0000"

    @patch("routes.openai.ChatCompletion.create")
    def test_palette_openai_error_returns_500(self, mock_create, client):
        mock_create.side_effect = Exception("API error")

        response = client.post("/palette", data={"query": "sunset"})
        assert response.status_code == 500
        json_data = response.get_json()
        assert "error" in json_data

    @patch("routes.openai.ChatCompletion.create")
    def test_palette_returns_variable_length(self, mock_create, client):
        """Verify the app passes through palettes of different sizes."""
        mock_response = MagicMock()
        mock_response.__getitem__ = lambda self, key: {
            "choices": [
                {"message": {"content": '["#EDF1D6", "#9DC08B", "#609966", "#40513B", "#2C3E50"]'}}
            ]
        }[key]
        mock_create.return_value = mock_response

        response = client.post("/palette", data={"query": "forest"})
        assert response.status_code == 200
        assert len(response.get_json()["colors"]) == 5
