from fastapi import FastAPI, WebSocket, Query
import os
import uuid
import logging
from .youtube_api import fetch_videos
from .detection import DeepfakeDetector, download_video

# Set up FastAPI
app = FastAPI()

# Initialize the deepfake detector
detector = DeepfakeDetector()

@app.get("/")
def home():
    return {"message": "Deepfake Detection API is running"}

@app.websocket("/ws/analyze")
async def analyze_videos(websocket: WebSocket, query: str = Query("deepfake", description="Search query for YouTube videos")):
    """Analyze YouTube videos for deepfake content."""
    await websocket.accept()  # Accept the WebSocket connection
    videos = fetch_videos(query=query)  # Fetch videos based on the search query

    for video in videos:
        logging.info(f"Processing video: {video['title']}")
        logging.info(f"URL: {video['url']}")

        video_filename = f"temp_{uuid.uuid4().hex}.mp4"
        video_path = os.path.abspath(os.path.join(os.getcwd(), video_filename))

        try:
            download_success = download_video(video['url'], video_path)

            if download_success:
                if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
                    is_deepfake = detector.detect_deepfake(video_path)
                    logging.info(f"Deepfake detection result for {video['title']}: {is_deepfake}")

                    # Send the result back to the client through WebSocket
                    await websocket.send_json({
                        "video": video['title'], 
                        "url": video['url'], 
                        "is_deepfake": bool(is_deepfake)
                    })
                else:
                    logging.error(f"Downloaded file is empty or does not exist: {video_path}")
            else:
                logging.error(f"Failed to download video: {video['title']}")
        except Exception as e:
            logging.error(f"Error processing video {video['title']}: {str(e)}")
        finally:
            if os.path.exists(video_path):
                os.remove(video_path)
                logging.info(f"Temporary file removed: {video_path}")
    
    await websocket.close()  # Close the WebSocket connection when done