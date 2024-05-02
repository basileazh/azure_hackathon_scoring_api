from io import BytesIO
from azure.storage.blob import BlobServiceClient

from hackathon_scoring_api.core.config import get_setting
from hackathon_scoring_api.core.log import logger


def get_blob(container: str, file_path: str) -> BytesIO:
    """
    Retrieves a Pandas dataframe from ADLS
    :param container: ADLS container name (ex: "sbx-trusted")
    :param file_path: ADLS file path in the container
    :return: Pandas dataframe
    """
    logger.info(f"Retrieving file {file_path} from container {container}")

    if get_setting("use_key_vault"):
        from hackathon_scoring_api.services.key_vault import retrieve_secret

        # OPTION 1 Here, we are attending to retrieve the ADLS access token from the key vault
        account_url = retrieve_secret(get_setting("adls_account_url_secret_name"))
        account_sas_token = get_setting("adls_account_sas_token_secret_name")
    else:
        # OPTION 2 Here, we are retrieving the ADLS tokens from environment variables
        account_url = get_setting("adls_account_url")
        account_sas_token = get_setting("adls_account_sas_token")

    # Create a blob service client
    blob_service_client = BlobServiceClient(
        account_url=account_url, credential=account_sas_token
    )
    logger.info("Created blob service client")

    # Download the ground truth file and convert to DataFrame
    file_content = BytesIO(
        blob_service_client.get_blob_client(container=container, blob=file_path)
        .download_blob()
        .readall()
    )
    logger.info(f"Downloaded file {file_path} from container {container}")

    return file_content
