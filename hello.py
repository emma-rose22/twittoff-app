from flask import Flask, render_template
from .models import DB, User, Tweet
app = Flask(__name__)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db.sqlite'
    DB.init_app(app)
    @app.route('/')
    def index():
      return 'Index Page'

    @app.route('/hello')
    def home():
      return render_template('base.html', title= 'Hello')
    return app

'''
if __name__=="__main__":
app.run(debug=True, port = 8080)
'''