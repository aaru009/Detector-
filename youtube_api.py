from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# YouTube API credentials
YOUTUBE_API_KEY = "AIzaSyB5R8lw2wvk54q5C0xC_jsIp0b_Jle7XqA"  # Replace with your actual API key

def create_youtube_client():
    """Create and return a YouTube API client."""
    try:
        return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    except Exception as e:
        print(f"An error occurred while creating the YouTube client: {e}")
        return None

def fetch_videos(query=" ", max_results=10):
    """Fetch latest videos based on the given query."""
    youtube = create_youtube_client()
    if not youtube:
        return []

    try:
        request = youtube.search().list(
            part="snippet",
            maxResults=max_results,
            type="video",
            order="date",
            q=query
        )
        response = request.execute()

        videos = []
        for item in response.get('items', []):
            video_title = item['snippet']['title']
            video_id = item['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append({'title': video_title, 'url': video_url})

        return videos

    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def main():
    query = input("Enter a search query (default is 'deepfake'): ") or "deepfake"
    videos = fetch_videos(query)
    
    if videos:
        print(f"\nFetched {len(videos)} videos for query '{query}':")
        for i, video in enumerate(videos, 1):
            print(f"{i}. Title: {video['title']}")
            print(f"   URL: {video['url']}\n")
    else:
        print("No videos found or an error occurred.")

if __name__ == "__main__":
    main()