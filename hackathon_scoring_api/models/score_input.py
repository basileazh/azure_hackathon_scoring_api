from pydantic import BaseModel
from typing import Dict, List, Optional, Union


class ScoreInput(BaseModel):
    team_id: str
    answers: Dict[str, List[Union[str, int]]]
    ground_truth: Optional[Dict[str, List[Union[str, int]]]] = None
    send_to_api: Optional[bool] = True
