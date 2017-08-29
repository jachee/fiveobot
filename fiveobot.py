"""
fiveobot.py - FiveOBot on twitter. It's five o'clock somewhere, every hour
or so.
"""

# from creds import *
import datetime, time, tweepy, creds

def check_time():
    now = datetime.datetime.today()
    return now.minute == 6

def tweet_out(phrase):
    # print("I would tweet now, if I were able.")
    auth = tweepy.OAuthHandler(creds.consumer_key, creds.consumer_secret)
    auth.set_access_token(creds.access_token, creds.access_token_secret)
    api = tweepy.API(auth)
    api.update_status(phrase)


def find_timezone():
    pass

def find_city():
    pass

def main():
    phrase = "Hello World!"
    while True:
        if check_time():
            tweet_out(phrase)
            time.sleep(60)



if __name__ == '__main__':
    main()
