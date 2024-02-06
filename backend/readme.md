alembic revision --autogenerate -m "initial migration"

# .env

HOST = "0.0.0.0"
BACKEND_PORT = 8000
RELOAD = True
DOCKER_PORT = 8000

# database
# ========

POSTGRES_USER='rishi'
POSTGRES_PASSWORD=12345
POSTGRES_DB='crud'
POSTGRES_HOST='db'
POSTGRES_DOCKER_PORT=5435

JWT_SECRET_KEY="apptoken"