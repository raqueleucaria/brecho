FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY backend/ . 
COPY entrypoint.sh /app/entrypoint.sh

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --with dev

# Certifique-se que o entrypoint.sh está na raiz do projeto (mesmo nível do Dockerfile)
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]