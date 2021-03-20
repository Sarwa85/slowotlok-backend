from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from flaskr.base import Base


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    source = Column(String)
    tr = Column(String)
    score = relationship("Score", uselist=False, backref="scores")

    def __init__(self, source, translation, score):
        self.source = source
        self.tr = translation
        self.score = score

    # Nie osądzaj mnie... 
    def to_dict(self):
        return {
            "id": self.id,
            "source": self.source,
            "tr": self.tr,
            "score": self.score.to_dict()
        }
