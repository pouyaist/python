# General:
import tweepy           # To consume Twitter's API
import pandas as pd     # To handle data
import numpy as np      # For number computing

# For plotting and visualization:
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
#matplotlib inline

# We import our access keys:
from credentials import *    # This will allow us to use the keys as variables

from textblob import TextBlob
import re

def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing 
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity == 0:
        return "Neutral"
    else:
        return "Negative"



# API's setup:
def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api







number_of_twitts = 20

# We create an extractor object:
extractor = twitter_setup()

print "Please enter twitter account name to Analyze. \nSuggestion:\trealDonaldTrump"
twitter_account_name = raw_input()


# We create a tweet list as follows:
tweets = extractor.user_timeline(screen_name=twitter_account_name, count=200)
print("Number of tweets extracted: {}.\n".format(len(tweets)))

# We print the most recent 5 tweets:
print "*****************************************************************************"
print str(number_of_twitts) + " recent tweets:\n" 
print "*****************************************************************************"
for tweet in tweets[:number_of_twitts]:
    print tweet.text
    print "------------------------------------------------------------" 

# We create a pandas dataframe as follows:
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])


# We add relevant data:
data['len']  = np.array([len(tweet.text) for tweet in tweets])
#data['ID']   = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])
data['SA'] = np.array([ analize_sentiment(tweet) for tweet in data['Tweets'] ])

print "*****************************************************************************"
# We display the first 10 elements of the dataframe:
display(data.head(number_of_twitts))


# We create time series for data:

tlen = pd.Series(data=data['len'].values, index=data['Date'])
tfav = pd.Series(data=data['Likes'].values, index=data['Date'])
tret = pd.Series(data=data['RTs'].values, index=data['Date'])

# Lenghts along time:
tlen.plot(figsize=(16,4), color='r')
#plt.show()


# Likes vs retweets visualization:
tfav.plot(figsize=(16,4), label="Likes", legend=True)
tret.plot(figsize=(16,4), label="Retweets", legend=True)
#plt.show()



# We obtain all possible sources:
sources = []
for source in data['Source']:
    if source not in sources:
        sources.append(source)


print "*****************************************************************************"
# We print sources list:
print("Creation of content sources:")
for source in sources:
    print("* {}".format(source))

# We create a numpy vector mapped to labels:
percent = np.zeros(len(sources))

for source in data['Source']:
    for index in range(len(sources)):
        if source == sources[index]:
            percent[index] += 1
            pass

percent /= 100

# Pie chart:
pie_chart = pd.Series(percent, index=sources, name='Sources')
pie_chart.plot.pie(fontsize=11, autopct='%.2f', figsize=(6, 6));
#plt.show()





# We construct lists with classified tweets:

pos_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] == "Positive"]
neu_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] == "Neutral"]
neg_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] == "Negative"]

# We print percentages:
print "*****************************************************************************"
print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(data['Tweets'])))
print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(data['Tweets'])))
print("Percentage de negative tweets: {}%".format(len(neg_tweets)*100/len(data['Tweets'])))	