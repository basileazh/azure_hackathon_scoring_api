from fastapi.testclient import TestClient
from hackathon_scoring_api.main import app

client = TestClient(app)


# Test the ping endpoint
def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


# Test the score endpoint
def test_score_accuracy():
    response = client.post("/score_accuracy/", json={
        "team_id": "test_team",
        "answers": {
            "id": [123, 456, 789, 159],
            "answer": ["a", "b", "a", "b"]
        },
        "ground_truth": {
            "id": [123, 456, 789, 159],
            "answer": ["a", "a", "a", "a"]
        },
        "send_to_api": "False",
    })
    print(response.json())
    # assert response.status_code == 200
    assert response.json() == {
        "accuracy_score": 0.5,
        "team_id": "test_team",
        # "submission_status": 200
    }


# Test the score endpoint with a missing ground truth
# def test_score_accuracy_missing_ground_truth():
#     response = client.post("/score_accuracy/", json={
#         "team_id": "test_team",
#         "answers": {
#             "index_1": [123, 456, 789, 159],
#             "index_2": ["x", "y", "z", "w"],
#             "answer": ["a", "b", "a", "b"]
#         },
#         "send_to_api": "False",
#     })
#     # assert response.status_code == 200
#     assert response.json() == {
#         "accuracy_score": 0.5,
#         "team_id": "test_team",
#         # "submission_status": 200
#     }
#
#
# def test_score_accuracy_missing_ground_truth_api_call():
#     response = client.post("/score_accuracy/", json={
#         "team_id": "653e7c5597196972f876b8cc",
#         "answers": {
#             "index_1": [123, 456, 789, 159],
#             "index_2": ["x", "y", "z", "w"],
#             "answer": ["a", "b", "a", "b"]
#         },
#     })
#     assert response.status_code == 200
#     assert response.json() == {
#         "accuracy_score": 0.5,
#         "team_id": "653e7c5597196972f876b8cc",
#         "submission_status": 200
#     }