import os

from app import db
from app import create_app
from flask_migrate import Migrate

from dotenv import dotenv_values

env = dotenv_values(".flaskenv")

app = create_app(env.get("FLASK_CONFIG"))
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    pass


@app.cli.command("init_db")
def init_db():
    pass


if __name__ == "__main__":
    app.run(threaded=True)
