import logging
import os
from pathlib import Path

path = Path(os.path.dirname(__file__))
basedir = os.path.abspath(str(path.parent.parent))


class Common(object):

    LOG_FILE = "/tmp/bank_api.log"
    LOG_LEVEL = logging.DEBUG

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
