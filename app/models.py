from core import db


class Repository(db.Document):
    """
    Main repository document to store data in MongoDB.
    """

    full_name = db.StringField()
    html_url = db.URLField()
    description = db.StringField()
    stargazers_count = db.IntField()
    language = db.StringField()

    meta = {'collection': 'repository'}


class Queue(db.Document):
    """
    Queue document serves as a global lock for upload jobs.
    """

    in_progress = db.BooleanField()

    meta = {'collection': 'queue'}
