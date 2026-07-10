import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from unittest.mock import MagicMock, patch
from db_client import CommanderDBClient


@patch("db_client.psycopg.connect")
class TestCreatePlayerTable:
    def test_creates_players_table(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__ = lambda s: mock_cursor
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        client = CommanderDBClient("postgresql://test")
        client.create_player_table()

        sql = mock_cursor.execute.call_args[0][0]
        assert "CREATE TABLE IF NOT EXISTS players" in sql

    def test_commits_after_create(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__ = lambda s: mock_cursor
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        client = CommanderDBClient("postgresql://test")
        client.create_player_table()

        mock_conn.commit.assert_called_once()


@patch("db_client.psycopg.connect")
class TestCreateCommanderTable:
    def test_creates_commanders_table(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__ = lambda s: mock_cursor
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        client = CommanderDBClient("postgresql://test")
        client.create_commander_table()

        sql = mock_cursor.execute.call_args[0][0]
        assert "CREATE TABLE IF NOT EXISTS commanders" in sql

    def test_commits_after_create(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__ = lambda s: mock_cursor
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        client = CommanderDBClient("postgresql://test")
        client.create_commander_table()

        mock_conn.commit.assert_called_once()


@patch("db_client.psycopg.connect")
class TestCreateDeckTable:
    def test_creates_decks_table(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__ = lambda s: mock_cursor
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        client = CommanderDBClient("postgresql://test")
        client.create_deck_table()

        sql = mock_cursor.execute.call_args[0][0]
        assert "CREATE TABLE IF NOT EXISTS decks" in sql

    def test_references_players_table(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__ = lambda s: mock_cursor
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        client = CommanderDBClient("postgresql://test")
        client.create_deck_table()

        sql = mock_cursor.execute.call_args[0][0]
        assert "REFERENCES players(player_id)" in sql

    def test_commits_after_create(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__ = lambda s: mock_cursor
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        client = CommanderDBClient("postgresql://test")
        client.create_deck_table()

        mock_conn.commit.assert_called_once()
