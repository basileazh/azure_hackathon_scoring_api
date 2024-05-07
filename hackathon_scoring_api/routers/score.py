import pandas as pd
import requests  # type: ignore
from fastapi import APIRouter, HTTPException

from collections.abc import Callable
import cryptpandas as crp

from hackathon_scoring_api.models.score_input import ScoreInput
from hackathon_scoring_api.services.adls import get_blob
from hackathon_scoring_api.core.config import get_setting
from hackathon_scoring_api.core.log import logger

router = APIRouter()  # Add prefix if needed


@router.post("/score_accuracy/")
async def score_accuracy(input_data: ScoreInput) -> dict[str, float | str]:
    team_id = input_data.team_id
    df_answers = pd.DataFrame(input_data.answers)
    send_to_api = input_data.send_to_api

    try:
        df_ground_truth = retrieve_ground_truth(input_data)

        assert df_answers.shape[0] == df_ground_truth.shape[0], (
            f"ShapeError rows : Number of rows in the answers {df_answers.shape[0]} "
            f"and ground truth {df_ground_truth.shape[0]} dataframes are not equal"
        )
        assert df_answers.shape[1] == df_ground_truth.shape[1], (
            f"ShapeError columns :Number of columns in the answers {df_answers.shape[1]} "
            f"and ground truth {df_ground_truth.shape[1]} dataframes are not equal"
        )
        assert set(df_answers.columns.tolist()) == set(
            df_ground_truth.columns.tolist()
        ), (
            f"ShapeError column names : Columns in the answers {set(df_answers.columns.tolist())} "
            f"and ground truth {set(df_ground_truth.columns.tolist())} dataframes are not equal"
        )

        # Set index to be able to merge the dataframes
        df_answers = df_answers.set_index(get_setting("index_colname"))
        df_ground_truth = df_ground_truth.set_index(get_setting("index_colname"))

        # Calculate accuracy score
        accuracy_score = calculate_accuracy_score(df_answers, df_ground_truth)

        # Send the score and team_id to another API
        if send_to_api:
            # payload = {"team_id": team_id, "accuracy_score": accuracy_score}
            # response = requests.put(get_setting("api_results_endpoint"), json=payload)

            api_url = get_setting("api_results_endpoint")
            api_url = api_url + f"?id={team_id}&score={accuracy_score}"
            response = requests.put(api_url, json={})

            return {
                "accuracy_score": accuracy_score,
                "team_id": team_id,
                "submission_status": response.status_code,
            }

        return {"accuracy_score": accuracy_score, "team_id": team_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_ground_truth(
    input_data: ScoreInput,
    container: str = get_setting("container"),
    file_path: str = get_setting("file_path"),
) -> pd.DataFrame:
    """
    Retrieves the ground truth data from the input data or from ADLS
    :param input_data: Data from the request
    :param container:  ADLS container name (ex: "sbx-trusted")
    :param file_path:  ADLS file path in the container (ex: "ground_truth/ground_truth_test.crypt")
    :return:         Pandas dataframe
    """
    if input_data.ground_truth is None:
        # Fetch the crypted ground truth data from ADLS
        df_ground_truth = get_ground_truth_data_from_adls(container, file_path)
    else:
        df_ground_truth = pd.DataFrame(input_data.ground_truth)

    return df_ground_truth


def get_ground_truth_data_from_adls(
    container: str,
    file_path: str,
    is_ground_truth_data_encrypted: bool = get_setting(
        "is_ground_truth_data_encrypted"
    ),
    cryptpandas_password: str = get_setting("cryptpandas_password"),
    reading_function: Callable = pd.read_csv,
):
    """
    Fetches the ground truth data for accuracy scoring
    :param container: ADLS container name (ex: "sbx-trusted")
    :param file_path: ADLS file path in the container
    :param is_ground_truth_data_encrypted: Whether the ground truth data is crypted or not
    :param cryptpandas_password: Password to decrypt the ground truth data
    :param reading_function: Function to read the ground truth data
    :return: Pandas dataframe
    """
    ground_truth_blob = get_blob(container, file_path)

    if is_ground_truth_data_encrypted:
        logger.info("Trying to decrypt data from blob using cryptpandas")
        # Write the ground truth data to a file
        with open("file.crypt", "wb") as f:
            f.write(ground_truth_blob.getvalue())

        # Decrypt the ground truth data
        ground_truth_df = crp.read_encrypted(
            path="file.crypt", password=cryptpandas_password
        )
    else:
        ground_truth_df = reading_function(ground_truth_blob, header=0)
        logger.info(
            f"Converted file {file_path} to Pandas dataframe using {reading_function.__name__}"
        )

    return ground_truth_df


def calculate_accuracy_score(df: pd.DataFrame, df_gc: pd.DataFrame) -> float:
    """
    Calculates the accuracy score between the answers and the ground truth
    :param df: Answers dataframe
    :param df_gc: Ground truth dataframe
    :return: Accuracy score
    """
    df_merged = pd.merge(df, df_gc, how="inner", left_index=True, right_index=True)
    assert df_merged.shape[0] == df_gc.shape[0], (
        f"ShapeError merge rows : The number of rows in the merged {df_merged.shape[0]} "
        f"and ground truth {df_gc.shape[0]} dataframes are not equal after the merge. "
        f"Original answers dataframe: {df.shape[0]}."
    )
    return len(df_merged[df_merged["answer_x"] == df_merged["answer_y"]]) / len(
        df_merged
    )
