import tweepy
import sys
from textblob import TextBlob
import matplotlib.pyplot as plt
import re
import  pandas as pd
import numpy as np

#defining the keys ---from twitter api
Consumer_Key = "qhfac9zsMmUCa8GkMLOYM21hg"
Consumer_Secret = "PNgSjpiu4rEHO2FkIri4mseCksGvxGFFbb0LluwrBUOhvtsGiI"
Access_token = "472099927-B03YMYZ8R88OTnQGIxvEN45mfrg2rNaUJNzP222K"
Access_token_Secret = "oE8fAROsHENZzCNfozla6z6t6elgllhU0eeRBBLi2Iovq"

#creating the authentication
auth = tweepy.OAuthHandler(consumer_key= Consumer_Key,consumer_secret=Consumer_Secret)
auth.set_access_token(Access_token,Access_token_Secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#asking user to enter the keyword and number of tweets to be analysed.
search_word = input("Enter the Keyword/hashtag to be searched:")
num_of_tweets = int(input("Enter the Number of tweets to be analysed:"))

#tweets = api.user_timeline(search_word,num_of_tweets,language = "english")
#tweets = tweepy.Cursor(api.search , q=search_word , language ="English").items()num_of_tweets

tweets = tweepy.Cursor(api.search , q=search_word , language ="English").items(num_of_tweets)
for tweet in tweets:
  analysis = TextBlob(tweet.text)
  polarity = analysis.sentiment.polarity  #At line
  #Creating the Data Frame of Tweets
  df = pd.DataFrame([tweet.text for tweet in tweets] , columns= ['Tweets'])
  #print(analysis)
  print(df.head())

#cleaning the tweets:
#cleaning all the unwanted stuff like hashtags,mentions,urls,etcc....by using re module we will do this.
def clean_tweet(txt):
  txt = re.sub('@[A-Za-z0–9]+', '', txt) #Removing @mentions
  txt = re.sub('#', '', txt) # Removing '#' hash tag
  txt = re.sub('RT[\s]+', '', txt) # Removing RT
  txt = re.sub('https?:\/\/\S+', '', txt) # Removing hyperlink
  return txt
#storing cleaned tweets by overiding the old one's by cleaning them.
df['Tweets'] = df['Tweets'].apply(clean_tweet)

#printing the cleaned tweets from the data frame. 
print(df.head())

#creating function to get the subjectivity.
def subjectivity(txt):
    return TextBlob(txt).sentiment.subjectivity
#creating a function to get the polarity
def t_polarity(txt):
    return TextBlob(txt).sentiment.polarity

#now creating two new columns in the created dataframe to store polarity and subjecttivity.

df['subjectivity'] = df['Tweets'].apply(subjectivity)
df['polarity'] = df['Tweets'].apply(t_polarity)
#displaying the new df with both subjectiviy and polarity
print(df.head())

#we have completed the cleaning and assigning the polarity task
def getAnalysis(score):
 if score < 0:
  return 'Negative'
 elif score == 0:
  return 'Neutral'
 else:
  return 'Positive'

df['Analysis'] = df['polarity'].apply(getAnalysis)
#printing positive tweets
print('Printing positive tweets:\n')
j=1
sortedD_Frame = df.sort_values(by=['polarity']) #Sorting the tweets
for i in range(0, sortedD_Frame.shape[0] ):
  if( sortedD_Frame['Analysis'][i] == 'Positive'):
    print(str(j) + ') '+ sortedD_Frame['Tweets'][i])
    print()
    j= j+1

# Printing negative tweets
print('Printing negative tweets:\n')
j=1
sortedDF = df.sort_values(by=['polarity'],ascending=False) #Sort the tweets
for i in range(0, sortedD_Frame.shape[0] ):
  if( sortedD_Frame['Analysis'][i] == 'Negative'):
    print(str(j) + ') '+sortedD_Frame['Tweets'][i])
    print()
    j=j+1
# Printing neutral tweets :
print('Printing negative tweets:\n')
j=1
sortedDF = df.sort_values(by=['polarity'],ascending=False) #Sort the tweets
for i in range(0, sortedD_Frame.shape[0] ):
  if( sortedD_Frame['Analysis'][i] == 'Neutral'):
    print(str(j) + ') '+sortedD_Frame['Tweets'][i])
    print()
    j=j+1
# Plotting
plt.figure(figsize=(10, 10))
for i in range(0, df.shape[0]):
  plt.scatter(df["polarity"][i], df["subjectivity"][i], color='Blue')  # plt.scatter(x,y,color)
plt.suptitle("\tHow People are reacting on "+ search_word + " by analysing "+ str(num_of_tweets) +" Tweets .")
plt.title('Sentiment Analysis')
plt.xlabel('polarity')
plt.ylabel('subjectivity')
plt.show()
