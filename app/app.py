from flask import Flask
from graphql_server.flask import GraphQLView
from schema import schema
from config import default
import logging
import os


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]: {} %(levelname)s %(message)s'
                    .format(
                        os.getpid()),
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger()


def create_app(config=default) -> Flask:
    app = Flask(__name__)
    app.config.from_object(f'config.{config}')
    # print(app.config)

    app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True if app.config.get(
            'FLASK_ENV') == 'development' else False
    ))

    return app


if __name__ == "__main__":
    app = create_app(default)
    app.run(debug=True, port=3000, host='0.0.0.0')
