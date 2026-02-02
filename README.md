# Patient Encounter System

This repository contains a minimal patient encounter API implemented with FastAPI, SQLAlchemy and Pydantic.

## Local development

Create and activate a virtual environment (optional) or use Poetry.

Install dependencies with Poetry:

```bash
poetry install
```

Run tests:

```bash
poetry run pytest -q
```

Run the app locally:

```bash
poetry run uvicorn src.main:app --reload
```

## Docker

Build the image:

```bash
docker build -t patient-encounter-system:latest .
```

Run the container:

```bash
docker run --rm -p 8000:8000 patient-encounter-system:latest
```
Smoke test (Linux/macOS):

```bash
curl -sSf http://127.0.0.1:8000/openapi.json
```

PowerShell (Windows) equivalent:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/openapi.json
```
## GitHub Actions CI/CD

This repository includes a CI workflow at `.github/workflows/ci.yml` which:

- Installs dependencies with Poetry
- Runs linters (`ruff`, `black`)
- Runs tests (`pytest`)
- Builds a Docker image and pushes to GitHub Container Registry (GHCR)

To allow GitHub to push the image to GHCR no extra secrets are required — the workflow uses the repository `GITHUB_TOKEN`.

If you prefer to deploy to a cloud provider, add a separate `deploy` workflow that consumes the built image or pushes to your cloud.

## Notes
- Ensure `pyproject.toml` and `poetry.lock` are present and correct.
- The pipeline expects Python 3.10.
