import os

from flask import Flask

import spatula.service.db.connection_factory as connection_factory


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # TODO - figure out provisioning scheme for this on non-local - probably env vars pulled from secrets manager
    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_USER='root',
        DB_PASSWORD='password',
        DB_HOST='127.0.0.1',
        DB_DATABASE='spatula',
        DB_PORT=3306
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    connection_factory.init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return {"db_result": connection_factory.get_db().cursor().execute("select 1")}

    return app