from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_deve_responder_sem_expor_debug() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["mensagem"]
    assert "debug" not in response.json()
    assert response.headers["x-content-type-options"] == "nosniff"


def test_health_deve_responder() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_rota_protegida_exige_token() -> None:
    response = client.get("/auth/me")
    assert response.status_code in {401, 403}
