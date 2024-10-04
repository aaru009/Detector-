import React from 'react';

function VideoList({ videos }) {
    if (videos.length === 0) {
        return;
    }

    return (
        <ul>
            {videos.map((video, index) => (
                <li key={index} className="video-item">
                    <p><strong>Title:</strong> {video.video}</p>
                    <p><strong>URL:</strong> <a href={video.url} target="_blank" rel="noopener noreferrer">Watch Video</a></p>
                    <p><strong>Deepfake:</strong> {video.is_deepfake ? "Yes" : "No"}</p>  {/* Display if it's a deepfake */}
                </li>
            ))}
        </ul>
    );
}

export default VideoList;