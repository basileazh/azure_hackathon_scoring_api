FROM python:3.9-slim
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

# Copy the current directory contents into the container
COPY . /app

# Set the working directory
WORKDIR /app
#ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip install --upgrade pip \
    && pip install poetry==1.5.1 \
    && poetry config virtualenvs.create false \
    && poetry install --without dev

# Run the command
EXPOSE 80
CMD ["python", "main.py"]