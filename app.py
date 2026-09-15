from flask import Flask
from models.conn import db
from models.model import seed_categories
from flask_migrate import Migrate

from blueprints.frontend import app as fe_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy_app.db'

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(fe_bp)

@app.cli.command("seed")
def seed():
    '''
    use this function from command line after flask db upgrade
    >flask seed
    '''
    seed_categories()
    print("Database seeded")

if __name__ == "__main__":
    app.run(debug=True)
