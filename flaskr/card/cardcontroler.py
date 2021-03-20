from flask import Blueprint, request, Response
from flaskr.card import cardservice
from flaskr.card.card import Card
from flaskr.score.score import Score

bp = Blueprint('card', __name__, url_prefix='/card')


@bp.route("", methods=['GET'])
def get_cards():
    order = request.args.get("order")
    limit = request.args.get("limit")
    return Response(response=cardservice.get_cards(order, limit), status=200, mimetype="application/json")


@bp.route("", methods=['POST'])
def add_card():
    j = request.json
    return cardservice.add_card(Card(j["source"], j["tr"], Score(0, 0)))


@bp.route("<card_id>", methods=["DELETE"])
def del_card(card_id):
    return cardservice.del_card(card_id)
