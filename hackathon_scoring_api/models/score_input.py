from pydantic import BaseModel


class ScoreInput(BaseModel):
    team_id: str
    answers: dict[str, list[str | int]]
    ground_truth: dict[str, list[str | int]] | None = None
    send_to_api: bool | None = True
