from decouple import config
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .predict import predict_user
from .twitter import add_or_update_user, update_all_users
#from dotenv import load_dotenv

#load_dotenv()

def create_app():
    """ creates an instance of the Flask application"""
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
    
    @app.route('/compare', methods=['POST'])
    def compare(message=''):
      user1 = request.values['user1']
      user2 = request.values['user2']
      tweet_text = request.values['tweet_text']

      if user1 == user2:
        message = "Silly, you can't compare a user to themselves! That would be boring."
      else:
        prediction = predict_user(user1, user2, tweet_text)
        message = '"{}" is more likely to be said by {} than {}'.format(
          request.values['tweet_text'], user1 if prediction else user2,
          user2 if prediction else user1)
        return render_template('predictions.html', title='Prediction', message=message)
    
    @app.route('/reset')
    def reset():
      '''wont be in final version'''
      DB.drop_all()
      DB.create_all()
      return render_template('base.html', title='Database Reset!')

    @app.route('/update')
    def update():
      update_all_users()
      return render_template('base.html', users=User.query.all(), title='Now we have all the latest tweets!')

    return app