import os
import sqlite3
import pytest

from database import (
    init_database,
    display_users,
    clear_test_data,
    anonymize_data
)


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """
    Creates a temporary database and overrides DATABASE_PATH
    """
    db_path = tmp_path / "test_users.db"
    monkeypatch.setenv("DATABASE_PATH", str(db_path))
    return db_path


def get_user_count(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_users(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


def test_init_database_creates_table_and_users(temp_db):
    init_database()

    # Verify users table exists and contains test data
    assert get_user_count(temp_db) == 2


def test_init_database_does_not_duplicate_users(temp_db, capsys):
    init_database()
    init_database()

    captured = capsys.readouterr()
    assert "Database already contains" in captured.out
    assert get_user_count(temp_db) == 2


def test_display_users_outputs_users(temp_db, capsys):
    init_database()

    display_users()

    captured = capsys.readouterr()
    assert "Current users in database" in captured.out
    assert "Matti Babalosi" in captured.out
    assert "Albin Kurden" in captured.out


def test_clear_test_data_removes_all_users(temp_db, capsys):
    init_database()
    clear_test_data()

    captured = capsys.readouterr()
    assert "All test data has been cleared" in captured.out
    assert get_user_count(temp_db) == 0


def test_anonymize_data_updates_all_users(temp_db, capsys):
    init_database()
    anonymize_data()

    users = get_users(temp_db)

    for name, email in users:
        assert name == "Anonym Användare"
        assert email == "Anonym@example.se"

    captured = capsys.readouterr()
    assert "anonymized" in captured.out.lower()
