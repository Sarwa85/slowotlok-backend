from flaskr.base import engine, Base


def init():
    Base.metadata.create_all(engine)
    print("database inited")

