from decouple import config
from flask import Flask, render_template
from .models import DB, User, Tweet
app = Flask(__name__)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCEMY_TRACK_MODIFICATIONS'] = False
    app.config['ENV'] = config('ENV') #change before deploying
    DB.init_app(app)
    @app.route('/')
    def index():
      return 'Index Page'

    @app.route('/')
    def home():
      users = User.query.all()
      return render_template('base.html', title='Home', users=users)

    def reset():
      '''wont be in final version'''
      DB.drop_all()
      DB.create_all()
      return render_template('base.html', title='DB Reset!', users=[])

    return app