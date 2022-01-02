from tweepy import OAuthHandler, API, Cursor
import tweepy 
# Enter your consumer key/access token pairs.
CONSUMER_KEY = 'client key'
CONSUMER_KEY_SECRET = 'client secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access secret'

# Handle Twitter OAuth
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# Wait if Twitter temporarily blocks requests
api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def parse(text):
    """
    Parses text for a twitter status and returns relevant action keywords.
    """
    twitter_actions = ['follow', 'retweet', 'rt', 'comment', 'like', 'fav']
    return [action for action in twitter_actions if action in text]


def perform_twitter_action(action, tweet_handle):
    """
    Given a list of twitter "action" keywords and a tweet handle (id),
    perform the specified action on the tweet handle.
    Example: perform_twitter_action("retweet", tweet_handle)
    -> Retweet the tweet specified by the tweet handle object
    :type action: string
    :type tweet_handle: tweepy Status object.
    """
    if action in ['retweet', 'rt']:
        api.retweet(tweet_handle.id)
    elif action in ['like', 'fav']:
        api.create_favorite(tweet_handle.id)
    elif action == 'follow':
        if 'retweeted_status' in tweet_handle._json:
            api.create_friendship(tweet_handle._json['retweeted_status']['user']['id'])
        else:
            api.create_friendship(tweet_handle._json['user']['id'])
    elif action == 'comment':
        api.update_status('Hmu please, I really want it', in_reply_to_status_id=tweet_handle.id)


def clear():
    """
    Clears all tweets from a twitter account.
    """
    for user_id in api.friends_ids():
        api.destroy_friendship(user_id)
    for i, tweet_handle in enumerate(Cursor(api.home_timeline).items()):
        api.destroy_status(tweet_handle.id)


def main():
    """
    Runs the script.
    """
    results = Cursor(api.search, q="chance to win").items(1000)
    for i, result in enumerate(results):
        actions = parse(result.text.lower())
        for action in actions:
            try:
                perform_twitter_action(action, result)
            except tweepy.error.TweepError:
                pass


if __name__ == '__main__':
    while True:
        main()
