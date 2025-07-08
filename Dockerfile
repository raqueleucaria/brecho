FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY backend/ . 

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --with dev


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
