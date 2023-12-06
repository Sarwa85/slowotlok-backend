import csv
from random import sample

from sqlalchemy import select, func

from flaskr.base import Session
from .card import Card
import json


def get_cards(order: str, limit: int):
    session = Session()
    query = session.query(Card)
    all_cards: [Card]

    # TODO obsłużyć to porządnie
    if order == "random" and limit:
        all_cards = query.order_by(func.random()).limit(limit)
    elif order == "random_lowest" and limit:
        stat_dict = {}
        all_cards = query.order_by(Card.bad.desc()).limit(limit * 4)
        for card in all_cards:
            stat_dict[card] = card.good - card.bad
        s_dict = sorted(stat_dict.items(), key=lambda p: p[1])
        all_cards = sample([item[0] for item in s_dict], limit)
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


# FIXME zwrócić Card
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
    if c := session.query(Card).get(card_id):
        session.delete(c)
        session.commit()
        return json.dumps(c.to_dict())
    return None


def update_card(card: Card):
    session = Session()
    c: Card = session.query(Card).filter(Card.id == card.id).first()
    c.good = card.good
    c.bad = card.bad
    c.tr = card.tr
    c.src = card.src
    session.commit()
    return json.dumps(card.to_dict())


def import_cards(card_list):
    session = Session()
    for card in card_list:
        session.add(card)
    session.commit()
    return
