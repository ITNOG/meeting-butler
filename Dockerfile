FROM python:3.13-slim

WORKDIR /app

COPY . .

# Install project dependencies using Poetry
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev 

# Set the entrypoint to run the application
ENTRYPOINT ["poetry", "run", "python", "-m", "meeting_butler"]
