import os
from flask import Flask
from models.conn import db
from models.model import seed_categories
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()   # da eseguire prima di importare blueprints o altri moduli dell'applicativo

from blueprints.frontend import app as fe_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)
# db.create_all() #creates all tables and constraints, DO NOT USE with Migrate

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
