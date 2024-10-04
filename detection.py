import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
import time
from .youtube_api import fetch_videos
from datetime import datetime
import uuid
import logging
import yt_dlp

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DeepfakeDetector:
    def __init__(self):
        self.model = self.load_model()

    def load_model(self):
        if os.path.exists('/Users/aryanpateriya/Desktop/Live Detection/backend/app/deepfake_detector_model_video.h5'):
            return load_model('/Users/aryanpateriya/Desktop/Live Detection/backend/app/deepfake_detector_model_video.h5')
        else:
            raise ValueError("No pre-trained model found. Please ensure the model file exists.")

    def preprocess_video(self, video_path, num_frames=20):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        frames = []
        frame_count = 0

        while len(frames) < num_frames:
            ret, frame = cap.read()
            if not ret:
                if len(frames) == 0:
                    raise ValueError(f"Could not read any frames from video: {video_path}")
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            if frame_count % 3 == 0:  # Sample every 3rd frame
                frame = cv2.resize(frame, (224, 224))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)
            
            frame_count += 1
        
        cap.release()
        frames = np.array(frames)
        frames = preprocess_input(frames)
        return np.expand_dims(frames, axis=0)  # Add batch dimension

    def detect_deepfake(self, video_path):
        processed_video = self.preprocess_video(video_path)
        prediction = self.model.predict(processed_video)
        return prediction[0][0] > 0.5  # Threshold of 0.5

def download_video(url, output_path):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logging.info(f"Video downloaded successfully: {output_path}")
        return True
    except Exception as e:
        logging.error(f"Error downloading video: {str(e)}")
        return False

def monitor_youtube():
    detector = DeepfakeDetector()
    
    while True:
        try:
            videos = fetch_videos()
            
            for video in videos:
                if not isinstance(video, dict) or 'title' not in video or 'url' not in video:
                    logging.warning(f"Skipping invalid video data: {video}")
                    continue

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
            
        except Exception as e:
            logging.error(f"An error occurred in the main loop: {str(e)}")
        
        logging.info("Waiting for 60 seconds before next iteration...")
        time.sleep(60)

if __name__ == "__main__":
    monitor_youtube()
    detector = DeepfakeDetector()