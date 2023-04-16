from app import create_app
from app import db
from dotenv import dotenv_values
from flask_migrate import Migrate

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
    app.run(threaded=True, port=5000, host="0.0.0.0")
