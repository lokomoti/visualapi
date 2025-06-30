# Use the official Python image from Docker Hub
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ENV ACCEPT_EULA=Y

# Install Microsoft ODBC Driver 17 for SQL Server
RUN apt-get update && \
    apt-get install -y curl gnupg apt-transport-https software-properties-common && \
    curl -sSL -O https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y msodbcsql17 mssql-tools unixodbc-dev libgssapi-krb5-2 iputils-ping && \
    rm -rf /var/lib/apt/lists/*

# Copy the project into the image
ADD . /app


# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --frozen --no-cache


CMD ["/app/.venv/bin/fastapi", "run", "/app/src/visualapi/main.py", "--port", "80"]