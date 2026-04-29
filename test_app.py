import pytest
import os
import tempfile
from app import app, init_db, DB_NAME


@pytest.fixture
def client():
    """Create a test client with a temporary database."""
    db_fd, temp_db = tempfile.mkstemp()
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret"

    import app as app_module
    original_db = app_module.DB_NAME
    app_module.DB_NAME = temp_db

    with app.test_client() as client:
        with app.app_context():
            app_module.init_db()
        yield client

    app_module.DB_NAME = original_db
    os.close(db_fd)
    os.unlink(temp_db)


def login(client, username="admin", password="admin"):
    """Helper to log in."""
    return client.post("/", data={"username": username, "password": password},
                       follow_redirects=True)


# ───────────────────────────────────────────
# AUTH TESTS
# ───────────────────────────────────────────

def test_login_page_loads(client):
    """Login page should return 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"ACEest" in response.data


def test_login_success(client):
    """Valid credentials should redirect to dashboard."""
    response = login(client)
    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_login_wrong_password(client):
    """Wrong password should show error."""
    response = client.post("/", data={"username": "admin", "password": "wrongpass"},
                           follow_redirects=True)
    assert b"Invalid credentials" in response.data


def test_login_wrong_username(client):
    """Wrong username should show error."""
    response = client.post("/", data={"username": "hacker", "password": "admin"},
                           follow_redirects=True)
    assert b"Invalid credentials" in response.data


def test_logout(client):
    """Logout should redirect to login page."""
    login(client)
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Sign In" in response.data


# ───────────────────────────────────────────
# DASHBOARD TESTS
# ───────────────────────────────────────────

def test_dashboard_requires_login(client):
    """Dashboard should redirect if not logged in."""
    response = client.get("/dashboard", follow_redirects=True)
    assert b"Sign In" in response.data


def test_dashboard_loads_after_login(client):
    """Dashboard should load after login."""
    login(client)
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_dashboard_shows_stats(client):
    """Dashboard should show client stats."""
    login(client)
    response = client.get("/dashboard")
    assert b"Total Clients" in response.data
    assert b"Active Members" in response.data


# ───────────────────────────────────────────
# CLIENT TESTS
# ───────────────────────────────────────────

def test_add_client(client):
    """Should be able to add a new client."""
    login(client)
    response = client.post("/clients/add", data={
        "name": "Test Client",
        "age": 25,
        "height": 175,
        "weight": 70,
        "program": "Fat Loss",
        "calories": 2000,
        "membership_end": "2025-12-31"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Client" in response.data


def test_add_client_requires_login(client):
    """Adding client should require login."""
    response = client.post("/clients/add", data={"name": "Test"},
                           follow_redirects=True)
    assert b"Sign In" in response.data


def test_client_detail_page(client):
    """Client detail page should load correctly."""
    login(client)
    client.post("/clients/add", data={
        "name": "Raj Kumar",
        "age": 28,
        "height": 170,
        "weight": 75,
        "program": "Muscle Gain",
        "calories": 3000
    })
    response = client.get("/client/Raj Kumar")
    assert response.status_code == 200
    assert b"Raj Kumar" in response.data


def test_client_not_found_redirects(client):
    """Non-existent client should redirect to dashboard."""
    login(client)
    response = client.get("/client/NonExistentPerson", follow_redirects=True)
    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_add_duplicate_client(client):
    """Adding duplicate client should not crash."""
    login(client)
    data = {"name": "Duplicate", "age": 25, "weight": 70,
            "height": 170, "program": "Beginner", "calories": 2000}
    client.post("/clients/add", data=data, follow_redirects=True)
    response = client.post("/clients/add", data=data, follow_redirects=True)
    assert response.status_code == 200


# ───────────────────────────────────────────
# WORKOUT TESTS
# ───────────────────────────────────────────

def test_add_workout(client):
    """Should be able to add a workout for a client."""
    login(client)
    client.post("/clients/add", data={
        "name": "Priya",
        "age": 22,
        "height": 162,
        "weight": 58,
        "program": "Fat Loss",
        "calories": 1800
    })
    response = client.post("/client/Priya/add_workout", data={
        "date": "2024-01-15",
        "type": "Cardio",
        "duration": 45,
        "notes": "Morning run"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Cardio" in response.data


def test_add_metric(client):
    """Should be able to add body metrics for a client."""
    login(client)
    client.post("/clients/add", data={
        "name": "Arjun",
        "age": 30,
        "height": 178,
        "weight": 85,
        "program": "Muscle Gain",
        "calories": 3200
    })
    response = client.post("/client/Arjun/add_metric", data={
        "date": "2024-01-15",
        "weight": 84.5,
        "waist": 90,
        "bodyfat": 18
    }, follow_redirects=True)
    assert response.status_code == 200


# ───────────────────────────────────────────
# PROGRAM GENERATOR TESTS
# ───────────────────────────────────────────

def test_generate_program(client):
    """Program generator should assign a program to client."""
    login(client)
    client.post("/clients/add", data={
        "name": "Meena",
        "age": 26,
        "height": 160,
        "weight": 62,
        "program": "Beginner",
        "calories": 1900
    })
    response = client.get("/client/Meena/generate_program", follow_redirects=True)
    assert response.status_code == 200
    assert b"Meena" in response.data


# ───────────────────────────────────────────
# API TESTS
# ───────────────────────────────────────────

def test_health_check(client):
    """Health endpoint should return 200 and healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert b"healthy" in response.data


def test_api_progress(client):
    """Progress API should return JSON data."""
    login(client)
    client.post("/clients/add", data={
        "name": "API Test Client",
        "age": 25,
        "height": 170,
        "weight": 70,
        "program": "Fat Loss",
        "calories": 2000
    })
    response = client.get("/api/progress/API Test Client")
    assert response.status_code == 200
    json_data = response.get_json()
    assert "weeks" in json_data
    assert "adherence" in json_data
    assert "weights" in json_data
