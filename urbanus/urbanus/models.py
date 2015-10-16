import dataset

from urbanus import settings


def db_connect():
    db = dataset.connect("sqlite:///{0}".format(settings.DATABASE_FILE_PATH))
    return db
