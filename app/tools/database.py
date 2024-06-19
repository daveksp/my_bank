from app.models import Account
from app.models import Person
from app.models import Transaction


DB_MODELS = [Account, Person, Transaction]


def recreate_db(db, bind='__all__', app=None):
    """
    Drop existing tables and create new ones according to the current schema.
    """
    db.drop_all(bind=bind, app=app)
    db.create_all(bind=bind, app=app)


def create_tables(db, bind='__all__', app=None):
    """
    Create all missing tables according to the current schema.
    """
    db.create_all()
