from dotenv import load_dotenv
import os
import requests
import pandas as pd
import numpy as np
from textblob import TextBlob
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import sys 

load_dotenv()

API_KEY=os.getenv("API_KEY")
BASE_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
VIDEO_ID=os.getenv('VIDEO_ID')

def fetch_comments(video_id, page_token=None):
    comments=[]
    params = {
        'part': 'snippet',
        'videoId': video_id,
        'key': API_KEY,
        'maxResults': 100  # you can set this to any value between 1 and 100
    }
    
    if page_token:
        params['pageToken'] = page_token

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    # Extract and print comments from the response
    for item in data['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)

    # Handle pagination: if there are more comments, fetch the next set
    if 'nextPageToken' in data:
        fetch_comments(video_id, page_token=data['nextPageToken'])
    print
    return comments

def convert_to_dataframe(comment_list):
    df = pd.DataFrame(comment_list,columns=['Comment'])
    return df

def combine_comments(comment_list_dataframe):
    combined_comment_string=''.join(comment_list_dataframe['Comment'])
    combined_string_df=pd.DataFrame([combined_comment_string],columns=['Comments'])
    return combined_string_df
    
#Create a function to get the subjectivity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

#Create a function to get the polarity
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

#Create a function to get the sentiment scores
def getSIA(text):
    sia = SentimentIntensityAnalyzer()
    sentiment=sia.polarity_scores(text)
    return sentiment

def get_sentiment_score(combined_comments_df,SIA):
    
    compound=(SIA['compound'])
    neg=(SIA['neg'])
    neu=(SIA['neu'])
    pos=(SIA['pos'])
    combined_comments_df['Compound']=compound
    combined_comments_df['Positive']=pos
    combined_comments_df['Negative']=neg
    combined_comments_df['Neutral']=neu
    return combined_comments_df

def main(video_id):
    video_id=video_id

    comment_list=fetch_comments(video_id)

    comment_list_df=convert_to_dataframe(comment_list)

    print("Comments : \n",comment_list_df)

    combined_comments_df=combine_comments(comment_list_df)

    combined_comments_df['Subjectivtiy']=combined_comments_df['Comments'].apply(getSubjectivity)

    combined_comments_df['Polarity']=combined_comments_df['Comments'].apply(getPolarity)

    SIA=getSIA(combined_comments_df['Comments'])

    comments_sentiment_df=get_sentiment_score(combined_comments_df,SIA)

    print("\nComments with Final Sentiment : \n",comments_sentiment_df)

    print("\nSentiment Score: ")
    print("Positive : ", (comments_sentiment_df['Positive'].astype(float)*100).round(5).values[0]," %")
    print("Negative : ", (comments_sentiment_df['Negative'].astype(float)*100).round(5).values[0]," %")
    print("Neutral : ", (comments_sentiment_df['Neutral'].astype(float)*100).round(5).values[0]," %")
    return {"Positive":str((comments_sentiment_df['Positive'].astype(float)*100).round(5).values[0])+" %",
            "Negative":str((comments_sentiment_df['Negative'].astype(float)*100).round(5).values[0])+" %",
            "Neutral" :str((comments_sentiment_df['Neutral'].astype(float)*100).round(5).values[0])+" %"}

if __name__ == "__main__":
    sys.exit(main(VIDEO_ID))