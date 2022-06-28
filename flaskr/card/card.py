from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from flaskr.base import Base


class Card(Base):
    __tablename__ = 'card'

    id = Column(Integer, primary_key=True)
    src = Column(String)
    tr = Column(String)
    good = Column(Integer)
    bad = Column(Integer)
    # score = relationship("Score", uselist=False, backref="card")

    def __init__(self, src, tr, good, bad, card_id=None,):
        self.id = card_id
        self.src = src
        self.tr = tr
        self.good = good
        self.bad = bad


    # def __init__(self, source, translation, good, bad):
    #     self.src = source
    #     self.tr = translation
    #     self.good = good
    #     self.bad = bad

    # Nie osądzaj mnie... 
    def to_dict(self):
        return {
            "id": self.id,
            "src": self.src,
            "tr": self.tr,
            "good": self.good,
            "bad": self.bad
        }
