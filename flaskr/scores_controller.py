import json
from flask import Blueprint, request, jsonify
from flaskr.repository import get_db
from dataclasses import dataclass

bp = Blueprint('logic1', __name__, url_prefix='/score')


@dataclass(init=True)
class Score:
    card_id: int
    good: int
    bad: int


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@bp.route("add", methods=['POST'])
def add_score():
    db = get_db()
    j = request.json
    score = Score(j["card_id"], j["good"], j["bad"])
    c = db.cursor()
    c.execute("SELECT id FROM cards WHERE id = ?", (score.card_id,))
    row = c.fetchone()
    if not row:
        return {"error": "bad id"}, 404

    c.execute("SELECT * FROM scores WHERE card_id = ?", (score.card_id,))
    score_row = c.fetchone()
    if score_row:
        c.execute("UPDATE scores SET good = good + ?, bad = bad + ? WHERE card_id = ?", (score.good, score.bad, score.card_id,))
        db.commit()
        if c.rowcount:
            c.execute("SELECT * FROM scores WHERE card_id = ?", (score.card_id,))
            row = c.fetchone()
            return jsonify(dict_factory(c, row)), 200
        else:
            return {"error", "can't insert score"}, 400
    else:
        c.execute("INSERT INTO scores (card_id, good, bad) VALUES (?, ?, ?)", (score.card_id, score.good, score.bad,))
        db.commit()
        if c.rowcount:
            return jsonify(score), 200
        else:
            return {"error", "can't insert score"}, 400
