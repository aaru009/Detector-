from fastapi import APIRouter
from .detection import detect_deepfake
from .youtube_api import fetch_videos

router = APIRouter()

#@router.get("/detect/tweets")
#async def detect_tweets():
    #tweets = fetch_tweets()
    #results = [detect_deepfake(tweet.media_url) for tweet in tweets]
    #return {"deepfakes": results}

@router.get("/detect/videos")
async def detect_videos():
    videos = fetch_videos()
    results = [detect_deepfake(video.media_url) for video in videos]
    return {"deepfakes": results}