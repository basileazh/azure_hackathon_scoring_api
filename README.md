# Scoring API for Hackathon

This application is intended to be used for scoring hackathon participants, 
at the end of their notebooks to submit their results.

## Usage

If you use Make, make sure you have a `.env` file with the following content:
    
```bash
DOCKER_IMAGE=hackathon-scoring-api
```

### Spin up the API

#### Using bash

```bash
poetry install
poetry run python hackathon_scoring_api/main.py
```

#### Using Docker

##### With Make

```bash
make install
dotenv -e environments/dev/.env make docker-start
```

##### Without Make

```bash
poetry install
docker build -t hackathon-scoring-api .
docker run -p 8080:8080 hackathon-scoring-api
```


### Endpoints

- `/ping` - GET - Returns a ping message
- `/score_accuracy` - POST - Returns an accuracy score for the given submission

### Example

```python
import requests

url = "http://localhost:8080/score_accuracy"

payload = {
    "submission": {
        "predictions": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        "labels": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    }
}
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, json=payload)

print(response.text)
```

## Requirements

- Python 3.9
- Poetry
- Docker
- FastAPI
- Uvicorn
- Pydantic

## Storing ground_truth in ADLS

### Environment variables

The installation depends on the way you store your ADLS credentials.
Required environment variables vary from the way you store ADLS credentials.

#### Option 1 : Using a service principal to access a key vault and retrieve the ADLS credentials

Environment variables:

- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `AZURE_TENANT_ID`
- `KEY_VAULT_URL`

Please set up the following secrets in your key vault:

- `adls-account-url-hackathon`
- `adls-account-sas-token-hackathon`

Using [poetry](https://python-poetry.org/) from command line:
```bash
poetry install
export  AZURE_CLIENT_ID=<your_azure_client_id>
export  AZURE_CLIENT_SECRET=<your_azure_client_secret>
export  AZURE_TENANT_ID=<your_azure_tenant_id>
export  KEY_VAULT_URL=<your_key_vault_url>
poetry run python hackathon_scoring_api/main.py
```

Using docker:
```bash
docker build -t hackathon-scoring-api --build-arg AZURE_CLIENT_ID=<your_azure_client_id> --build-arg AZURE_CLIENT_SECRET=<your_azure_client_secret> --build-arg AZURE_TENANT_ID=<your_azure_tenant_id> --build-arg KEY_VAULT_URL=<your_key_vault_url> .
docker run -p 8080:8080 hackathon-scoring-api
```

#### Option 2 : Directly using the ADLS credentials in the environment variables

Environment variables:

- `ADLS_ACCOUNT_URL`
- `ADLS_ACCOUNT_SAS_TOKEN`

Using [poetry](https://python-poetry.org/) from command line:
```bash
poetry install
export ADLS_ACCOUNT_URL=<your_adls_account_name>
export ADLS_ACCOUNT_SAS_TOKEN=<your_adls_account_sas_token>
poetry run python main.py
```

Using docker:
```bash
docker build -t hackathon-scoring-api --build-arg ADLS_ACCOUNT_URL=<your_adls_account_name> --build-arg ADLS_ACCOUNT_SAS_TOKEN=<your_adls_account_sas_token> .
docker run -p 8080:8080 hackathon-scoring-api
```
