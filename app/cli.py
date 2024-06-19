from flask import Blueprint

from app.extensions import db
from app.tools.database import create_tables as create_tables_helper
from app.tools.database import recreate_db as recreate_db_helper


bp = Blueprint('cli', __name__, cli_group=None)


@bp.cli.group()
def database():
    pass


@database.command()
def create_tables():
    """Creates the database tables"""
    print("init database")
    create_tables_helper(db)


@database.command()
def rebuilddb_command():
    """Rebuilds the database structure"""
    print("init database")
    recreate_db_helper(db)
