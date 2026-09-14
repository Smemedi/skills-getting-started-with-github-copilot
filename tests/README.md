# Backend Tests

Comprehensive test suite for the FastAPI application using pytest.

## Running Tests

### Run all tests with verbose output
```bash
pytest tests/ -v
```

### Run a specific test file
```bash
pytest tests/test_activities.py -v
```

### Run a specific test class
```bash
pytest tests/test_signup.py::TestSignup -v
```

### Run a specific test
```bash
pytest tests/test_signup.py::TestSignup::test_signup_successful -v
```

### Run tests with coverage report
```bash
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
```

## Test Organization

### `test_activities.py`
Tests for the `GET /activities` endpoint.

**Coverage:**
- Returns 200 status code
- Returns a dictionary of activities
- Contains all expected activities
- Each activity has required fields (description, schedule, max_participants, participants)
- Participants field is a list
- Initial participant count is correct

### `test_signup.py`
Tests for the `POST /activities/{activity_name}/signup` endpoint.

**Coverage:**
- Successful signup (200 status, correct message)
- Participant is added to the activity
- Non-existent activity returns 404
- Duplicate signup returns 400
- Same student can signup for different activities
- Activity names with spaces work correctly
- Integration: activities list reflects signup immediately

### `test_unregister.py`
Tests for the `POST /activities/{activity_name}/unregister` endpoint.

**Coverage:**
- Successful unregister (200 status, correct message)
- Participant is removed from the activity
- Non-existent activity returns 404
- Unregister for student not signed up returns 400
- Cannot unregister twice returns 400
- Cannot unregister from activity student isn't in
- Integration: activities list reflects unregister immediately
- Full flow: signup → unregister

## Test Fixtures

All tests use fixtures from `conftest.py`:

- **`activities_data`**: Provides a fresh copy of the activities database for each test
- **`client`**: Provides a FastAPI TestClient with isolated state

State isolation ensures tests don't interfere with each other. The fixture automatically:
1. Replaces the app's activities with test data before each test
2. Restores the original state after each test

## Test Statistics

- **Total Tests**: 21
- **Test Files**: 3
- **Test Classes**: 3
- **All Tests Passing**: ✓

### Breakdown by Endpoint
- `GET /activities`: 6 tests
- `POST /signup`: 7 tests
- `POST /unregister`: 8 tests

## Adding New Tests

1. Add test method to appropriate class in `tests/test_*.py`
2. Use `client` fixture to make requests
3. Use `activities_data` fixture to access initial data
4. Follow naming convention: `test_<feature>_<scenario>`

Example:
```python
def test_signup_with_special_characters_in_email(self, client):
    """Test signup with special characters in email."""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "user+tag@mergington.edu"}
    )
    assert response.status_code == 200
```

## Requirements

- Python 3.8+
- pytest
- FastAPI
- uvicorn
- httpx

Install all dependencies:
```bash
pip install -r requirements.txt
```
