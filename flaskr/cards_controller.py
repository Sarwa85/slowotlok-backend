from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import func
from .models import Card
from .extensions import db

cards_bp = Blueprint('logic', __name__, url_prefix='/card')


@cards_bp.route("", methods=['POST'])
def add_card():
    j = request.json
    card = Card(source=j["source"], tr=j["tr"])
    db.session.add(card)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error, 400
    return card.to_dict(), 200


@cards_bp.route("", methods=['GET'])
def get_cards():
    cards = Card().query.all()
    out = [card.to_dict() for card in cards]
    return jsonify(out), 200


@cards_bp.route("<card_id>", methods=['GET'])
def get_card(card_id):
    card = Card.query.get(card_id)
    if card:
        return jsonify(card.to_dict()), 200
    else:
        return {"error": "wrong id"}, 400


@cards_bp.route("<card_id>", methods=['DELETE'])
def del_card(card_id):
    try:
        Card.query.filter_by(id=card_id).delete()
    except SQLAlchemyError as e:
        return {"error": str(e.__dict__['orig'])}, 400
    return {"removed": card_id}, 200


@cards_bp.route("", methods=['PATCH'])
def patch_card():
    j = request.json
    try:
        card = Card.query.get(j["id"])
        card.source = j["source"]
        card.tr = j["tr"]
        db.session.commit()
    except SQLAlchemyError as e:
        return {"error": str(e.__dict__['orig'])}, 400
    return card.to_dict(), 200


@cards_bp.route("/random/<int:count>", methods=['GET'])
def random_cards(count):
    cards = Card().query.order_by(func.random()).limit(10).all()
    return jsonify(list([card.to_dict() for card in cards])), 200
