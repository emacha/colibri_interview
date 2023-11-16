"""Test the API endpoints."""
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "I'm working!"}


class TestGetAll:
    """Test the GET /v1/persons endpoint."""

    def test_get_all(self):
        """Test that we can get all persons."""
        response = client.get("/v1/persons")
        assert response.status_code == 200
        # 1000 is the default page size
        assert len(response.json()["persons"]) == 1000

    def test_pagination(self):
        """Test that we can paginate."""
        response = client.get("/v1/persons?offset=0&page_size=2")
        middle = response.json()["persons"][1][1]
        response = client.get("/v1/persons?offset=1&page_size=2")
        assert response.json()["persons"][0][1] == middle

    def test_sort(self):
        """Test that we can sort the persons."""
        response = client.get("/v1/persons?sort_by=first_name")
        assert response.status_code == 200
        assert response.json()["persons"][0][1] == "Aarika"

    def test_sort_desc(self):
        """Test that we can sort the persons in descending order."""
        response = client.get("/v1/persons?sort_by=first_name&ascending=false")
        assert response.status_code == 200
        assert response.json()["persons"][0][1] == "Zsazsa"

    def test_sort_injection(self):
        """Test that we can't pass invalid values to sort_by."""
        response = client.get("/v1/persons?sort_by=bobby_tables")
        assert response.status_code == 422

    def test_filter(self):
        """Test that we can filter the persons."""
        response = client.post("/v1/persons", json={"industry": "Metal Fabrications"})
        assert response.status_code == 200
        assert response.json()["persons"][0][6] == "Metal Fabrications"


def test_get_one():
    """Test the GET /v1/persons/{id} endpoint."""
    response = client.get("/v1/persons/1")
    assert response.status_code == 200
    assert response.json()["person"][0] == 1


def test_update_one():
    """Test the PATCH /v1/persons/{id} endpoint."""
    response = client.get("/v1/persons/1")
    assert response.json()["person"][1] == "Annmarie"
    response = client.patch("/v1/persons/1", json={"first_name": "Marianne"})
    assert response.status_code == 200
    response = client.get("/v1/persons/1")
    assert response.json()["person"][1] == "Marianne"


def test_delete_one():
    """Test the DELETE /v1/persons/{id} endpoint."""
    response = client.get("/v1/persons/1")
    assert response.status_code == 200
    response = client.delete("/v1/persons/1")
    assert response.status_code == 200
    response = client.get("/v1/persons/1")
    assert response.status_code == 200
    assert response.json()["person"] is None


class TestAverage:
    """Test the GET /v1/average endpoint."""

    def test_age_per_industry(self):
        """Test the first average case."""
        response = client.get("/v1/average?column=age&per=industry")
        assert response.status_code == 200
        averages = response.json()["average"]
        assert averages[1] == ["Advertising", 63.0]

    def test_salary_per_industry(self):
        """Test the second average case."""
        response = client.get("/v1/average?column=salary&per=industry")
        assert response.status_code == 200
        averages = response.json()["average"]
        assert int(averages[1][1]) == 124518

    def test_salary_per_years_of_experience(self):
        """Test the third average case."""
        response = client.get("/v1/average?column=salary&per=years_of_experience")
        assert response.status_code == 200
        averages = response.json()["average"]
        assert int(averages[1][1]) == 133644

    def test_injection(self):
        """Test that we can't pass invalid values to column."""
        response = client.get("/v1/average?column=bobby_tables&per=years_of_experience")
        assert response.status_code == 422
