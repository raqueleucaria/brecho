FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY backend/ . 

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --with dev


EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "src.app:app"]