# Frontend

## Run Project

### With Backend (Full Setup)

1. in folder **cs50-moodle-bridge** run ```docker-compose -f docker-compose.dev.yml up -d```
2. in folder **frontend** run ```uv run streamlit run src/app.py```

### Standalone (Mock Mode - No Backend Required)

Run the frontend with sample data for testing and development without needing the backend:

- Option 1: Use the quick start script

```bash
./run_mock.sh
```

- Option 2: Set environment variable
  
```
USE_MOCK_SERVICES=true uv run streamlit run src/app.py
```

## Frontend Testing

### Run all tests

```bash
uv run pytest
```

### Run only unit tests

```bash
uv run pytest -m unit
```

### Run tests with coverage

```bash
uv run pytest --cov=src --cov-report=html
```

## .env Configuration Options

```python

# Enable mock services (set to "true" to use mocks, "false" to use real backend)
USE_MOCK_SERVICES=true

# API Configuration (not used when USE_MOCK_SERVICES=true, but kept for reference)
API_BACKEND_URL=http://localhost:8000
API_TIMEOUT=30

LOG_LEVEL=INFO
```
