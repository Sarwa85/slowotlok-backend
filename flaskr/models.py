from .extensions import db


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column("id", db.Integer, primary_key=True)
    source = db.Column("source", db.Unicode, unique=True, nullable=False)
    tr = db.Column("tr", db.Unicode, nullable=False)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # def __init__(self, card_source, card_tr):
    #     self.source = card_source
    #     self.tr = card_tr

    def __repr__(self):
        return "<Card %s %s %s >" % (self.id, self.source, self.tr)

    def to_dict(self):
        return {"id": self.id, "source": self.source, "tr": self.tr}


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, unique=True,)
    good = db.Column(db.Integer)
    bad = db.Column(db.Integer)

    def __repr__(self):
        return "<Score %s %s %s %s>" % (self.id, self.card_id, self.good, self.bad)


def init_model(app):
    app.cli.add_command(init_model)




