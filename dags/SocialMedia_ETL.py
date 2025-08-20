from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from googleapiclient.discovery import build
import tweepy
from tweepy import Paginator
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()  

YouTube_api_key = os.getenv("YOUTUBE_API_KEY")
Twitter_Bearer_Token = os.getenv("TWITTER_BEARER_TOKEN")

def extract_tweets():
    client = tweepy.Client(bearer_token= Twitter_Bearer_Token)
    q="a -is:retweet"
    fields=["created_at", "public_metrics", "author_id"]
    tweets_list = []

    for tweet in Paginator(
        client.search_recent_tweets,
        query=q,
        tweet_fields=fields,
        max_results=10 
    ).flatten(limit=50):
        tweets_list.append(tweet)

    return tweets_list


def extract_videos():
    youtube = build('youtube', 'v3', developerKey= YouTube_api_key)

    search_resp = youtube.search().list(
        q="data engineering",
        part= "snippet",
        type= "video",
        maxResults= 50 
    ).execute()

    videos_lists=[]

    for item in search_resp.get("items",[]):
        video_id = item["id"]["videoId"]

        stats_response= youtube.videos().list(
            part = "statistics,snippet",
            id = video_id
        ).execute()

        video = stats_response["items"][0]
        videos_lists.append(video)

    return videos_lists


def transform_data(ti):
    tweets_list = ti.xcom_pull(task_ids="extract_tweets")
    videos_lists= ti.xcom_pull(task_ids= "extract_videos")
    transformed_data = []

    for tweet in tweets_list:
        likes = tweet.public_metrics.get("like_count", 0)
        comments = tweet.public_metrics.get("reply_count", 0)
        retweets = tweet.public_metrics.get("retweet_count", 0)
    
        transformed_data.append({
            "Content": tweet.text,
            "Likes": likes,
            "Comments": comments,
            "Shares/Retweets": retweets,
            "Engagement_Score": likes + comments + retweets,
            "Post date/time": tweet.created_at,
            "Platform": "Twitter",
            "Author/User ID": tweet.author_id
        })

    for video in videos_lists:
        Likes= int(video["statistics"].get("likeCount",0))
        Comments= int(video["statistics"].get("commentCount",0))

        transformed_data.append({
            "Content" : video["snippet"]["title"],
            "Likes" : Likes,
            "Comments" : Comments,
            "Shares/Retweets" : 0,
            "Engagement_Score": Likes + Comments,
            "Date_Posted" : pd.to_datetime(video["snippet"]["publishedAt"],utc=True),
            "Platform" : "Youtube",
            "Author_id" : video["snippet"]["channelId"]
        })

    df = pd.DataFrame(transformed_data)
    ti.xcom_push(key="social_df", value=df.to_dict(orient="records"))


def load_data(ti):
    social_data = ti.xcom_pull(task_ids= "transform_data", key="social_df")
    df = pd.DataFrame(social_data)
    df.to_csv("./SocialMedia_Analysis.csv" , index=False, encoding = "utf-8")
    print("Saved ", len(df), " records to CSV")


def analyze_data():
    df = pd.read_csv("./SocialMedia_Analysis.csv")

    df["Date_Posted"] = pd.to_datetime(df["Date_Posted"])
    df["Date"] = df["Date_Posted"].dt.date
    
    daily_engagement = df.groupby(["Platform", "Date"])["Engagement_Score"].sum().reset_index()
    daily_engagement["Report_Type"] = "Daily_Engagement"

    top5 = df.sort_values("Engagement_Score", ascending=False).head(5)
    top5["Report_Type"] = "Top5_Overall"

    top3_platform = df.groupby("Platform").apply(
        lambda x: x.sort_values("Engagement_Score", ascending=False).head(3)
    ).reset_index(drop=True)
    top3_platform["Report_Type"] = "Top3_Per_Platform"

    combined = pd.concat([daily_engagement, top5, top3_platform], ignore_index=True, sort=False)
    combined.to_csv("./Analytics_Report.csv", index=False, encoding="utf-8")

    print("Analytics saved in a single file: Analytics_Report.csv")


with DAG('SocialMedia_ETL' , start_date =datetime(2025,8,20) ,
          schedule_interval='@daily' , catchup = False) as dag:
    
    extract_tweets_task = PythonOperator(
        task_id="extract_tweets",
        python_callable=extract_tweets,
    )

    extract_videos_task = PythonOperator(
        task_id="extract_videos",
        python_callable=extract_videos,
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
    )

    load_task = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
    )

    analyze_task = PythonOperator(
        task_id="analyze_data",
        python_callable=analyze_data,
    )

    [ extract_tweets_task >> extract_videos_task ] >> transform_task >> load_task >> analyze_task
