import os

from flask_migrate import Migrate

from app import create_app
from app.exts import db

app = create_app(os.environ.get("FLASK_CONFIG"))
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    pass


@app.cli.command("init_db")
def init_db():
    pass


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
