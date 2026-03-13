from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_transcript(video_id):
    """
    Extract transcript from YouTube video using video ID.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        str: Transcript text or None if not available
    """
    try:
        # Try to get transcript in English first
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        
        # Join all text parts
        text = " ".join([t["text"] for t in transcript])
        
        # Clean up the text
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
        
    except Exception as e:
        # Try to get any available language if English is not available
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_manually_created_transcript()
            
            if transcript:
                transcript_data = transcript.fetch()
                text = " ".join([t["text"] for t in transcript_data])
                text = re.sub(r'\s+', ' ', text).strip()
                return text
                
        except Exception:
            pass
            
        return None

def extract_video_id(url):
    """
    Extract video ID from YouTube URL.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: Video ID or None if not found
    """
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
        r'youtube\.com/watch\?.*v=([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None
