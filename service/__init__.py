from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/odyca'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['STATIC_FOLDER'] = "./static/"
app.config['SECRET_KEY'] = 'secret_key'
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
app.app_context().push()

from service import routes