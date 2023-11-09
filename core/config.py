import os
from enum import Enum
import pandas as pd

from .log import logger


class Settings(Enum):
    """
    Settings for the application
    """
    # ## API settings ## #
    api_results_endpoint = "xxx"

    # ## Data settings ## #
    is_ground_truth_data_encrypted = True
    cryptpandas_password = "xxx"

    # ## Score settings ## #
    index_colname = "id"
    predictions_colname = "answer"

    # ## Key Vault ## #
    use_key_vault = False
    if (use_key_vault) & ("USE_KEY_VAULT" in os.environ.keys()):
        logger.info("Retrieved USE_KEY_VAULT from environment variables")
        key_vault_name = os.environ["KEY_VAULT_NAME"]
        key_vault_uri = f"https://{key_vault_name}.vault.azure.net"

    # ## ADLS settings ## #
    # OPTION 1 This is the key where the secret is supposed to be stored in the key vault. used if use_key_vault is True
    adls_account_url_secret_name = "xxx"
    adls_account_sas_token_secret_name = "xxx"

    # OPTION 2 Retrieving from environment variables. used if use_key_vault is False
    if "ADLS_ACCOUNT_URL" in os.environ.keys():
        logger.info("Retrieved ADLS_ACCOUNT_URL from environment variables")
        adls_account_url = os.environ["ADLS_ACCOUNT_URL"]
    if "ADLS_ACCOUNT_SAS_TOKEN" in os.environ.keys():
        logger.info("Retrieved ADLS_ACCOUNT_SAS_TOKEN from environment variables")
        adls_account_sas_token = os.environ["ADLS_ACCOUNT_SAS_TOKEN"]

    # Ground truth data for accuracy scoring
    container = "xxx"
    file_path = "xxx.crypt"


def get_setting(setting):
    return Settings[setting].value
