# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY pyproject.toml /app

# Install Poetry
RUN pip install poetry

# Install project dependencies using poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy the content of the local src directory to the working directory
COPY src/app /workdir

# Expose the port that FastAPI will run on
EXPOSE 8000
