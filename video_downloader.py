from pytube import YouTube
import os

def download_video(video_url: str, save_path: str) -> bool:
    
    try:
        # Create the YouTube object
        yt = YouTube(video_url)
        
        # Select the highest resolution stream available
        stream = yt.streams.get_highest_resolution()
        
        # Download the video
        stream.download(output_path=os.path.dirname(save_path), filename=os.path.basename(save_path))
        
        print(f"Downloaded: {yt.title}")
        return True
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return False