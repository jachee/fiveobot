"""
fiveobot.py - FiveOBot on twitter. It's five o'clock somewhere, every hour
or so.
"""

# from creds import *
import datetime, time, tweepy, creds

def check_time():
    now = datetime.datetime.utcnow()
    return now.minute == 0

def tweet_out(phrase):
    # print("I would tweet now, if I were able.")
    auth = tweepy.OAuthHandler(creds.consumer_key, creds.consumer_secret)
    auth.set_access_token(creds.access_token, creds.access_token_secret)
    api = tweepy.API(auth)
    print(phrase)
    api.update_status(phrase)


def tz_phrase():
    gmt = datetime.datetime.utcnow()
    if gmt.hour >= 0 and gmt.hour <= 5:
        offset = 17 - gmt.hour - 24
        if offset >= 0:
            offstr = ''.join(['+', str(offset)])
        else:
            offstr = str(offset)
    else:
        offset = 17 - gmt.hour
        if offset >= 0:
            offstr = ''.join(['+', str(offset)])
        else:
            offstr = str(offset)


    return "It's five o'clock somewhere! Currently UTC %s" % offstr

def find_city():
    pass

def main():
    while True:
        if check_time():
            phrase = tz_phrase()
            tweet_out(phrase)
        time.sleep(55)



if __name__ == '__main__':
    main()
