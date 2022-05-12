from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flaskr.base import Base


class Score(Base):
    __tablename__ = 'score'

    id = Column(Integer, primary_key=True)
    good = Column(Integer)
    bad = Column(Integer)
    card_id = Column(Integer, ForeignKey('card.id'))

    def __init__(self, good: int, bad: int) -> None:
        self.good = good
        self.bad = bad

    def to_dict(self):
        return {
            "id": self.id,
            "good": self.good,
            "bad": self.bad
        }
