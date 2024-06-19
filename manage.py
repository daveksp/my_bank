import sqlalchemy as sa
import sqlalchemy.orm as so

from app import create_app
from app.extensions import db
from app.models import Account
from app.models import Person
from app.models import Transaction

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'sa': sa, 
        'so': so, 
        'db': db, 
        'Account': Account, 
        'Person': Person, 
        'Transaction': Transaction
    }
