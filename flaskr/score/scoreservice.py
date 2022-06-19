from sqlalchemy import select, func

from flaskr.base import Session
import json

from flaskr.score.score import Score


def add_score(card_id: int, good: int, bad: int):
    session = Session()
    score = session.query(Score).filter(Score.card_id == card_id).first()
    if score:
        print("Jest score")
        score.good = good
        score.bad = bad
        session.commit()
        return json.dumps(score.to_dict())
    return None
