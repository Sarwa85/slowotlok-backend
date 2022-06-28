import csv

from sqlalchemy import select, func

from flaskr.base import Session
from .card import Card
import json


def get_cards(order, limit):
    session = Session()
    query = session.query(Card)
    all_cards: [Card]

    # TODO obsłużyć to porządnie
    if order == "random" and limit:
        all_cards = query.order_by(func.random()).limit(limit)
    else:
        all_cards = query.all()
    return json.dumps(list([card.to_dict() for card in all_cards]))


def get_card(id: int):
    session = Session()
    query = session.query(Card)
    card: [Card] = query.filter(Card.id == id).first()
    return json.dumps(card.to_dict())


def get_all_cards():
    session = Session()
    query = session.query(Card)
    all_cards: [Card] = query.all()
    return json.dumps(list([card.to_dict() for card in all_cards]))


def add_card(card: Card):
    session = Session()
    session.add(card)
    session.commit()
    # session.close()
    return json.dumps(card.to_dict())


def get_random(count: int):
    session = Session()
    random_cards = session.query(Card).order_by(func.random()).limit(count)
    return json.dumps(list([card.to_dict() for card in random_cards]))


def del_card(card_id: int):
    session = Session()
    c = session.query(Card).filter(Card.id == card_id)
    c.delete()
    session.commit()
    return c


def update_card(card: Card):
    session = Session()
    c: Card = session.query(Card).filter(Card.id == card.id).first()
    c.good = card.good
    c.bad = card.bad
    c.tr = card.tr
    c.src = card.src
    session.commit()
    return card


def import_cards(card_list):
    session = Session()
    for card in card_list:
        session.add(card)
    session.commit()
    return
