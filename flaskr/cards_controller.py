import json
from flask import Blueprint, request
from flaskr.repository import get_db
from dataclasses import dataclass
# from flask_api import status

bp = Blueprint('logic', __name__, url_prefix='/card')


@dataclass(init=True)
class Card:
    id: int
    source: str
    tr: str


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@bp.route("", methods=['POST'])
def add_card():
    db = get_db()
    j = request.json
    sr = j["source"]
    tr = j["tr"]
    if db.execute("SELECT id FROM cards WHERE source = ?", (sr,)).fetchone():
        return {"error": "wpis istnieje już w bazie"}

    c = db.cursor()
    c.execute("INSERT INTO cards (source, tr) VALUES(?,?)", (sr, tr,))
    db.commit()
    card = Card(c.lastrowid, sr, tr)
    return json.dumps(card.__dict__)


@bp.route("", methods=['GET'])
def get_cards():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM cards")
    rows = c.fetchall()
    out = []
    for row in rows:
        out.append(dict_factory(c, row))
    return json.dumps(out)


@bp.route("<id>", methods=['GET'])
def get_card(id):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM cards WHERE id = ?", (id,))
    row = c.fetchone()
    if row:
        return json.dumps(dict_factory(c, row))
    else:
        return "Niepoprawne id", 404



# /card - random
# DELETE /card/<id>
# PATCH /card/<id>

# POST /score/<id>
# GET /score/<id>
# GET /scores