FROM python:3.10-slim
LABEL authors="basile.elazhari"

# Setup build args
ARG AZURE_TENANT_ID
ARG AZURE_CLIENT_ID
ARG AZURE_CLIENT_SECRET
ARG KEY_VAULT_NAME
ARG ADLS_ACCOUNT_URL
ARG ADLS_ACCOUNT_SAS_TOKEN


# Set environment variables
ENV AZURE_TENANT_ID=${AZURE_TENANT_ID}
ENV AZURE_CLIENT_ID=${AZURE_CLIENT_ID}
ENV AZURE_CLIENT_SECRET=${AZURE_CLIENT_SECRET}
ENV KEY_VAULT_NAME=${KEY_VAULT_NAME}
ENV ADLS_ACCOUNT_URL=${ADLS_ACCOUNT_URL}
ENV ADLS_ACCOUNT_SAS_TOKEN=${ADLS_ACCOUNT_SAS_TOKEN}

# Set the working directory
WORKDIR /app
ENV PYTHONPATH /app

# Copy the current directory contents into the container
COPY pyproject.toml poetry.lock ./
COPY hackathon_scoring_api ./hackathon_scoring_api


RUN pip install --upgrade pip \
    && pip install poetry==1.7.0 \
    && poetry config virtualenvs.create false \
    && poetry install

# Run the command
EXPOSE 8080
CMD ["poetry", "run", "python", "hackathon_scoring_api/main.py"]