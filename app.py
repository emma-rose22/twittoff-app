from decouple import config
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user
app = Flask(__name__)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
      DB.create_all()
      return render_template('base.html', title='Home', users=User.query.all())
    
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
      name= name or request.values['username']
      try:
        if request.method== 'POST':
          add_or_update_user(name)
          message= f'User {name} successfully added!'
        tweets = User.query.filter(User.name==name).one().tweets
      except Exception as e:
        message = f'Error while trying to add user {name}: {e}'
        tweets = []
      return render_template('user.html', title=name, message =message, tweets=tweets)
    
    @app.route('/reset')
    def reset():
      '''wont be in final version'''
      DB.drop_all()
      DB.create_all()
      return render_template('base.html', title='Database Reset!')

    return app