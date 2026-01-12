# Frontend

## run Project
1. in folder **cs50-moodle-bridge** run ```docker-compose -f docker-compose.dev.yml up -d```
2. in folder **frontend** run ```uv run streamlit run src/pages/streamlit_app.py ```


## Frontend Testing

### Run all tests:
```bash
uv run pytest
```

### Run only unit tests:
```bash
uv run pytest -m unit
```

### Run tests with coverage:
```bash
uv run pytest --cov=src --cov-report=html
```

### Run specific test file:
```bash
uv run pytest tests/unit/services/test_course_service.py
```

### Run specific test:
```bash
uv run pytest tests/unit/services/test_course_service.py::test_get_courses_returns_list_on_success
```