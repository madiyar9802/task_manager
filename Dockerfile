FROM python:3.11.0

RUN mkdir /app
WORKDIR /app
COPY . .

RUN pip3 install poetry
RUN poetry install
RUN poetry add alembic sqlalchemy psycopg2-binary

EXPOSE 5002
CMD ["poetry", "python run.py", "app"]