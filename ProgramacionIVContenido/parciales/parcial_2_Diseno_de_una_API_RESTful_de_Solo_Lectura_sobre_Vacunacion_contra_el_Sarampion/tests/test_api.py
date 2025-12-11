from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_all_vaccines_returns_data():
    response = client.get("/vacunas")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) >= 1
    first = payload[0]
    assert set(first.keys()) == {"year", "country", "indicator", "coverage"}


def test_get_vaccine_by_year_success():
    response = client.get("/vacunas/2005")
    assert response.status_code == 200
    assert response.json()["year"] == 2005


def test_get_vaccine_by_year_not_found():
    response = client.get("/vacunas/1999")
    assert response.status_code == 404


def test_get_provincial_data_defaults_to_latest_year():
    response = client.get("/vacunas/provincia/Panamá")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["province"].lower() == "panamá"
    assert "coverage" in data[0]


def test_get_provincial_data_by_year():
    response = client.get("/vacunas/provincia/Los%20Santos?year=2010")
    assert response.status_code == 200
    data = response.json()
    assert all(entry["year"] == 2010 for entry in data)


def test_get_provincial_data_not_found():
    response = client.get("/vacunas/provincia/Atlantida")
    assert response.status_code == 404
