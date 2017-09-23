'''
fiveobot.py - FiveOBot on twitter. It's five o'clock somewhere, every hour
or so. 

Timezone data from https://timezonedb.com 
  CC By 3.0 https://creativecommons.org/licenses/by/3.0/

Geographic data from https://data.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000%40public/information
  CC By 3.0 http://creativecommons.org/licenses/by/3.0/
'''

import calendar, datetime, time, tweepy, creds, sqlite3, random

def check_time():
    now = datetime.datetime.utcnow()
    return now.minute == 0

def tweet_out(phrase):
    auth = tweepy.OAuthHandler(creds.consumer_key, creds.consumer_secret)
    auth.set_access_token(creds.access_token, creds.access_token_secret)
    api = tweepy.API(auth)
    print(phrase)
    api.update_status(phrase)

def tz_offset():
    utc = datetime.datetime.utcnow()
    if utc.hour >= 0 and utc.hour <= 5:
        offset = 17 - utc.hour - 24
    else:
        offset = 17 - utc.hour
    return offset * 3600

def find_city(zones, cur):
    zone = random.choice(zones)
    query = 'SELECT "ASCII Name", "Country" FROM  geonames WHERE Timezone=?'
    cityobj = cur.execute(query, (zone,))
    cities = cityobj.fetchall()
    return random.choice(cities)

def find_zones(offset, cur):
    ''' Finds the Region/City style name(s) that match a given timezone
        offset from .  Expects an integer for seconds offset,
        Returns a list of strings.'''

    query = ('SELECT DISTINCT z.zone_name '
             'FROM timezone tz JOIN zone z ON tz.zone_id=z.zone_id '
             'WHERE tz.time_start <= strftime("%s", "now") '
             'AND tz.gmt_offset=? ORDER BY tz.time_start')

    zoneobj = cur.execute(query, (offset,))
    zones = []
    for row in zoneobj.fetchall():
        zones.append(row[0])
    return zones

def main():
    conn = sqlite3.connect('tzdb.sqlite3')
    cur = conn.cursor()
    while True:
        if check_time():
            phrase = "It's five o'clock somewhere! "
            offset = tz_offset()
            zones = find_zones(offset, cur)
            city = find_city(zones, cur)
            print(city)
            phrase = phrase + "For example: %s, %s!" % city
            tweet_out(phrase)
            time.sleep(60)



if __name__ == '__main__':
    main()
