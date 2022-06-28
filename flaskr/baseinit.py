from flaskr.base import engine, Base
from flaskr.card import card
# from flaskr.score import score


def init():
    Base.metadata.create_all(engine)
    print("database inited")

