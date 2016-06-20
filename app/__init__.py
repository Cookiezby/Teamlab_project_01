from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.debug = True
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app import views, models
