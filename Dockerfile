FROM python:3.12-slim 
ENV POETRY_VIRTUAL_ENVS_CREATE=false

WORKDIR /app 
COPY . .
COPY --chmod=755 ./entrypoint.sh /app

RUN pip install poetry

RUN poetry config installer.max-workers 10 
RUN poetry install --no-interaction --no-ansi 

EXPOSE 8000
CMD poetry run uvicorn app.main:app --host 0.0.0.0

