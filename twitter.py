#retreive tweets, embedddigns, and persist in database
import tweepy, basilica
from decouple import config
from .models import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                    config('TWITTER_CONSUMER_SECRET'))
                    
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                            config('TWITTER_ACCESS_TOKEN_SECRET'))

TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))

def add_or_update_user(name):
    """
    add or update a user and their Tweets.
    Throw an error if user doesn't exist or is private.
    """
    try:
        DB.session(autoflush=False)
        twitter_user= TWITTER.get_user(name)
        db_user = (User.query.get(twitter_user.id) or User(id=twitter_user.id, name=name))
        DB.session.add(db_user)
        tweets = twitter_user.timeline(count=200, 
                                       exclude_replies=True, 
                                       include_rts=False, 
                                       since_id=db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id=tweets[0].id
        for tweet in tweets:
            embedding = BASILICA.embed_sentence(tweet.text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.text[:500], embedding=embedding)
            DB.session.add(db_tweet)
            db_user.tweets.append(db_tweet)
    except Exception as e:
        print(f'Encountered error while processing {name}: {e}')
        raise e
    else:
        DB.session.commit()

