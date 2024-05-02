import pandas as pd
import pytest
from fastapi import HTTPException

from routers.score import (
    retrieve_ground_truth,
    calculate_accuracy_score,
    get_ground_truth_data_from_adls,
    score_accuracy,
)
from hackathon_scoring_api.models.score_input import ScoreInput


def test_calculate_accuracy_score():
    df_answers = pd.DataFrame({
        "id": [123, 456, 789, 159],
        "answer": ["a", "b", "a", "b"]
    })
    ground_truth_df = pd.DataFrame({
        "id": [123, 456, 789, 159],
        "answer": ["a", "a", "a", "a"]
    })
    accuracy_score = calculate_accuracy_score(df_answers, ground_truth_df)
    assert accuracy_score == 0.5


def test_retrieve_ground_truth_from_score_input():
    input_data = ScoreInput(
        team_id="test_team",
        answers={
            "id": [123, 456, 789, 159],
            "answer": ["a", "b", "a", "b"]
        },
        ground_truth={
            "id": [123, 456, 789, 159],
            "answer": ["a", "a", "a", "a"]
        },
        send_to_api="False",
    )
    df_ground_truth = retrieve_ground_truth(
        input_data,
        container="dev-raw",
        file_path="ground_truth/ground_truth_test.crypt"
    )

    assert df_ground_truth.shape == (4, 2)


def test_retrieve_ground_truth_from_adls():
    input_data = ScoreInput(
        team_id="test_team",
        answers={
            "id": [123, 456, 789, 159],
            "answer": ["a", "b", "a", "b"]
        },
        ground_truth=None,
        send_to_api="False",
    )
    df_ground_truth = retrieve_ground_truth(
        input_data,
        container="dev-raw",
        file_path="ground_truth/ground_truth_test.crypt"
    )

    assert df_ground_truth.shape == (4, 2)


def test_get_ground_truth_data_from_adls():
    ground_truth_df = get_ground_truth_data_from_adls(
        container="dev-raw",
        file_path="ground_truth/ground_truth_test.crypt",
        is_ground_truth_data_encrypted=True,
        cryptpandas_password="oRBK}uvhK3C;Ndr"
    )

    assert ground_truth_df.shape == (4, 2)


@pytest.mark.asyncio
async def test_score_accuracy():
    response = await score_accuracy(
        ScoreInput(
            team_id="test_team",
            answers={
                "id": [123, 456, 789, 159],
                "answer": ["a", "b", "a", "b"]
            },
            ground_truth={
                "id": [123, 456, 789, 159],
                "answer": ["a", "a", "a", "a"]
            },
            send_to_api="False",
        )
    )
    assert response == {
        "accuracy_score": 0.5,
        "team_id": "test_team",
        # "submission_status": 200
    }


@pytest.mark.asyncio
async def test_score_accuracy_wrong_rows():
    # Case missing rows
    try:
        response = await score_accuracy(
            ScoreInput(
                team_id="test_team",
                answers={
                    "id": [123, 456, 789],
                    "answer": ["a", "b", "a"]
                },
                ground_truth={
                    "id": [123, 456, 789, 159],
                    "answer": ["a", "a", "a", "a"]
                },
                send_to_api="False",
            )
        )
    except HTTPException as e:
        assert e.status_code == 500
        assert str(e.detail).startswith("ShapeError rows")

    # Case extra rows
    try:
        response = await score_accuracy(
            ScoreInput(
                team_id="test_team",
                answers={
                    "id": [123, 456, 789, 159, 357],
                    "answer": ["a", "b", "a", "b", "a"]
                },
                ground_truth={
                    "id": [123, 456, 789, 159],
                    "answer": ["a", "a", "a", "a"]
                },
                send_to_api="False",
            )
        )
    except HTTPException as e:
        assert e.status_code == 500
        assert str(e.detail).startswith("ShapeError rows")

    # case wrong rows
    try:
        response = await score_accuracy(
            ScoreInput(
                team_id="test_team",
                answers={
                    "id": [123, 456, 789, 159],
                    "answer": ["a", "b", "a", "b"]
                },
                ground_truth={
                    "id": [123, 456, 789, 150],
                    "answer": ["a", "a", "a", "a"]
                },
                send_to_api="False",
            )
        )
    except HTTPException as e:
        assert e.status_code == 500
        assert str(e.detail).startswith("ShapeError merge rows")


@pytest.mark.asyncio
async def test_score_accuracy_wrong_columns():
    # Case missing columns
    try:
        response = await score_accuracy(
            ScoreInput(
                team_id="test_team",
                answers={
                    "id": [123, 456, 789, 159],
                    "answer": ["a", "b", "a", "b"]
                },
                ground_truth={
                    "id": [123, 456, 789, 159],
                },
                send_to_api="False",
            )
        )
    except HTTPException as e:
        assert e.status_code == 500
        assert str(e.detail).startswith("ShapeError columns")

    # Case extra columns
    try:
        response = await score_accuracy(
            ScoreInput(
                team_id="test_team",
                answers={
                    "id": [123, 456, 789, 159],
                    "answer": ["a", "b", "a", "b"]
                },
                ground_truth={
                    "id": [123, 456, 789, 159],
                    "answer": ["a", "a", "a", "a"],
                    "extra_column": ["a", "a", "a", "a"]
                },
                send_to_api="False",
            )
        )
    except HTTPException as e:
        assert e.status_code == 500
        assert str(e.detail).startswith("ShapeError columns")

    # Case wrong columns
    try:
        response = await score_accuracy(
            ScoreInput(
                team_id="test_team",
                answers={
                    "id": [123, 456, 789, 159],
                    "answer": ["a", "b", "a", "b"]
                },
                ground_truth={
                    "id": [123, 456, 789, 159],
                    "wrong_column": ["a", "a", "a", "a"]
                },
                send_to_api="False",
            )
        )
    except HTTPException as e:
        assert e.status_code == 500
        assert str(e.detail).startswith("ShapeError column names")
