FROM python:${PYTHON_VERSION}-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY pyproject.toml ./poetry.lock /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Pull official base image
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
CMD ["pytest"]
