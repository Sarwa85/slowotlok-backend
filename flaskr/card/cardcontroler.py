import csv
import json

from flask import Blueprint, request, Response
from flask_login import login_required

from flaskr.card import cardservice
from flaskr.card.card import Card
# from flaskr.score.score import Score

bp = Blueprint('card', __name__, url_prefix='/card')


@bp.route("/<card_id>", methods=['GET'])
# @login_required
def get_card(card_id: int):
    return Response(response=cardservice.get_card(card_id), status=200, mimetype="application/json")


@bp.route("", methods=['GET'])
# @login_required
def get_cards():
    return Response(response=cardservice.get_all_cards(), status=200, mimetype="application/json")


@bp.route("<order>/<limit>", methods=['GET'])
def get_ordered_cards(order, limit: int):
    return Response(response=cardservice.get_cards(order, int(limit)), status=200, mimetype="application/json")



@bp.route("", methods=['POST'])
def add_card():
    j = request.json
    card = Card(src=j["src"], tr=j["tr"], good=0, bad=0)
    return Response(response=cardservice.add_card(card), status=200, mimetype="application/json")


@bp.route("", methods=['PUT'])
def update_card():
    j = request.json
    card = Card(src=j["src"], tr=j["tr"], good=j["good"], bad=j["bad"], card_id=j["id"])
    return Response(response=json.dumps(cardservice.update_card(card).to_dict()), status=200, mimetype="application/json")


@bp.route("<card_id>", methods=["DELETE"])
def del_card(card_id):
    return Response(response=cardservice.del_card(card_id), status=200, mimetype="application/json")


# TODO Dekorator z content-type
@bp.route("import", methods=["POST"])
def import_cards():
    cards = [Card(row[0], row[1], 0, 0) for row in csv.reader(request.data.decode("UTF-8").splitlines(), delimiter=';', quotechar='|')]
    return Response(response=cardservice.import_cards(cards), status=200, mimetype="application/json")
