import json
from flask import Blueprint, request, jsonify
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
    return jsonify(card.__dict__), 200


@bp.route("", methods=['GET'])
def get_cards():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT cards.id, "
              "cards.source, "
              "cards.tr, "
              "COALESCE(scores.good, 0) as good, "
              "COALESCE(scores.bad, 0) as bad "
              "FROM cards "
              "LEFT JOIN scores ON cards.id=scores.id")
    rows = c.fetchall()
    out = []
    for row in rows:
        out.append(dict_factory(c, row))
    return jsonify(out), 200


@bp.route("<card_id>", methods=['GET'])
def get_card(card_id):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
    row = c.fetchone()
    if row:
        return jsonify(dict_factory(c, row)), 200
    else:
        return "Niepoprawne id", 404


@bp.route("<id>", methods=['DELETE'])
def del_card(id):
    db = get_db()
    c = db.cursor()
    c.execute("DELETE FROM cards WHERE id = ?", (id,))
    db.commit()
    if c.rowcount:
        return {"removed": id}, 200
    else:
        return ("Nie usunięto %s" % id), 404


@bp.route("", methods=['PATCH'])
def patch_card():
    db = get_db()
    j = request.json
    card_id = j["id"]
    sr = j["source"]
    tr = j["tr"]
    c = db.cursor()
    c.execute("UPDATE cards SET source = ?, tr = ? WHERE id = ?", (sr, tr, card_id))
    db.commit()
    if c.rowcount:
        return j, 200
    else:
        return ("Nie zaktualizowano %s" % card_id), 404


@bp.route("/random/<int:count>", methods=['GET'])
def random_cards(count):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT cards.id, "
              "cards.source, "
              "cards.tr, "
              "COALESCE(scores.good, 0) as good, "
              "COALESCE(scores.bad, 0) as bad "
              "FROM cards "
              "LEFT JOIN scores ON cards.id=scores.card_id "
              "ORDER BY RANDOM() LIMIT ?", (count,))
    rows = c.fetchall()
    out = []
    for row in rows:
        out.append(dict_factory(c, row))
    return jsonify(out), 200


# POST /score/<id>
# GET /score/<id>
# GET /scores