import csv
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas

#Twitter API Keys (Enter keys provided by Twitter) 
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

#Enter number of tweets to be streamed
tweet_limit = 1000
#Enter topic or list of topics to be streamed
tracklist = "covid-19"

tweet_count = 0
tweet_data = []


#Class that will handle the twitter stream
class StdOutListener(StreamListener):
      
    def on_data(self, data):
        global tweet_count
        global tweet_limit
        global stream
        if tweet_count < tweet_limit:
            tweet = json.loads(data)
            try:
                  tweet_data.append(str(tweet["text"]))
                  #Optional print
                  print(tweet["text"] + tweet["created_at"])
                  tweet_count += 1
            except:
                  print("An exception has occured")
            return True
        else:
            stream.disconnect()
        

    def on_error(self, status):
        print(status)


if __name__ == '__main__':  
    #Handle Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(consumer_key, consumer_secret)
    l = StdOutListener()
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(languages = ['en'], track=tracklist)
    
    #Save text of tweets to csv file in working directory 
    df = pandas.DataFrame(tweet_data)
    df.to_csv(r'stream_data.csv', index = False, header = False)
