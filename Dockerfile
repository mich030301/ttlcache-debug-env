FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace
COPY pyproject.toml README.md ./
COPY src ./src
COPY tests ./tests
COPY tasks ./tasks
RUN pip install -e ".[dev]"

CMD ["python", "tasks/verify.py"]
