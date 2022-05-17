import csv

from flask import Blueprint, request, Response
from flaskr.card import cardservice
from flaskr.card.card import Card
from flaskr.score.score import Score

bp = Blueprint('card', __name__, url_prefix='/card')


@bp.route("<order>/<limit>", methods=['GET'])
def get_cards(order, limit):
    return Response(response=cardservice.get_cards(order, limit), status=200, mimetype="application/json")


@bp.route("", methods=['POST'])
def add_card():
    j = request.json
    return Response(response=cardservice.add_card(Card(j["source"], j["tr"], Score(0, 0))), status=200, mimetype="application/json")


@bp.route("<card_id>", methods=["DELETE"])
def del_card(card_id):
    return Response(response=cardservice.del_card(card_id), status=200, mimetype="application/json")


# TODO Dekorator z content-type
@bp.route("import", methods=["POST"])
def import_cards():
    cards = [Card(row[0], row[1], Score(0, 0)) for row in csv.reader(request.data.decode("UTF-8").splitlines(), delimiter=';', quotechar='|')]
    return Response(response=cardservice.import_cards(cards), status=200, mimetype="application/json")
