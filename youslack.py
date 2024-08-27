import os
from googleapiclient.discovery import build
import datetime
import requests
import logging
import isodate
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# YouTube API setup
YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Slack webhook URL
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']

# List of channel IDs to monitor
CHANNEL_IDS = [
    'UC_ywfvIR2JrnMuZt33y7QYQ',
    'UCtehAp4VxQSHrbNvVHEZ89g',
    'UCESLZhusAkFfsNsApnjF_Cg',
    'UCV00elXN8Z0vrFIAZu3rIKw',
    'UC-_tUpRdhh7Qc3vn6FFbhGw'
]

def get_latest_video(channel_id):
    try:
        eight_hours_ago = (datetime.utcnow() - timedelta(hours=8)).isoformat() + 'Z'
        search_response = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            order='date',
            type='video',
            publishedAfter=eight_hours_ago,
            maxResults=1
        ).execute()
        
        if not search_response['items']:
            return None
        
        video_id = search_response['items'][0]['id']['videoId']
        
        video_response = youtube.videos().list(
            part='contentDetails',
            id=video_id
        ).execute()
        
        duration = video_response['items'][0]['contentDetails']['duration']
        duration_seconds = isodate.parse_duration(duration).total_seconds()
        
        if duration_seconds <= 60:
            logging.info(f"Video {video_id} is a short, skipping")
            return None
        
        return search_response['items'][0]
    except Exception as e:
        logging.error(f"Error fetching video for channel {channel_id}: {str(e)}")
        return None

def send_slack_message(video):
    title = video['snippet']['title']
    video_id = video['id']['videoId']
    message = {
        "text": f"New video uploaded: {title}\nhttps://www.youtube.com/watch?v={video_id}"
    }
    
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        response.raise_for_status()
        logging.info(f"Slack message sent for video: {title}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending Slack message: {str(e)}")

def test_script():
    logging.info("Starting test run")
    for channel_id in CHANNEL_IDS:
        logging.info(f"Testing channel: {channel_id}")
        latest_video = get_latest_video(channel_id)
        if latest_video:
            logging.info(f"Latest video found: {latest_video['snippet']['title']} (https://www.youtube.com/watch?v={latest_video['id']['videoId']})")
            send_slack_message(latest_video)
        else:
            logging.info(f"No suitable videos found for channel {channel_id}")
    logging.info("Test run completed")

if __name__ == '__main__':
    test_script()