from flask import Blueprint, request, Response

from flaskr.score import scoreservice

bp = Blueprint('score', __name__, url_prefix='/score')


@bp.route("add", methods=['POST'])
def add_score():
    j = request.json
    return Response(response=scoreservice.add_score(j["card_id"], j["good"], j["bad"]), status=200, mimetype="application/json")
