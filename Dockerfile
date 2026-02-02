FROM python:3.10-slim

# set a working directory
WORKDIR /app

# install system deps
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl git && rm -rf /var/lib/apt/lists/*

# install poetry
RUN python -m pip install --upgrade pip && pip install poetry

# copy project files
COPY pyproject.toml poetry.lock* ./

# install dependencies (no root package to avoid packaging errors)
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# copy source
COPY src ./src
COPY README.md ./README.md

# expose port and default command
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
