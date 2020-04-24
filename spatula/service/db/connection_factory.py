import MySQLdb
from flask import current_app, g


def get_db():
    if 'db' not in g:
        # Flask uses g as global request scoped state - this allows reusing conns across one request
        g.db = MySQLdb.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_DATABASE'],
            port=current_app.config['DB_PORT'])
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
