import re
from typing import List

def split_text(text: str, chunk_size: int = 2000, overlap: int = 100) -> List[str]:
    """
    Split long text into chunks with overlap for better summarization.
    
    Args:
        text (str): Input text to split
        chunk_size (int): Maximum size of each chunk
        overlap (int): Number of characters to overlap between chunks
        
    Returns:
        List[str]: List of text chunks
    """
    if not text:
        return []
    
    # Clean up text first
    text = re.sub(r'\s+', ' ', text).strip()
    
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        # Calculate end position
        end = start + chunk_size
        
        # If this is the last chunk, take whatever remains
        if end >= len(text):
            chunks.append(text[start:])
            break
        
        # Try to break at a sentence boundary
        chunk = text[start:end]
        
        # Look for sentence endings near the end of chunk
        sentence_endings = ['. ', '! ', '? ', '.\n', '!\n', '?\n']
        best_break = -1
        
        for i in range(len(chunk) - 1, max(0, len(chunk) - 200), -1):
            if chunk[i:i+2] in sentence_endings:
                best_break = i + 2
                break
        
        if best_break > 0:
            chunks.append(chunk[:best_break])
            start = start + best_break - overlap
        else:
            # No good sentence break, just split at chunk_size
            chunks.append(chunk)
            start = end - overlap
    
    return chunks

def clean_transcript(text: str) -> str:
    """
    Clean transcript text by removing artifacts.
    
    Args:
        text (str): Raw transcript text
        
    Returns:
        str: Cleaned transcript text
    """
    if not text:
        return ""
    
    # Remove common transcript artifacts
    text = re.sub(r'\[.*?\]', '', text)  # Remove [music], [applause] etc.
    text = re.sub(r'\(.*?\)', '', text)  # Remove (laughs), (coughs) etc.
    text = re.sub(r'\s+', ' ', text)     # Replace multiple spaces with single space
    text = text.strip()
    
    return text

def extract_video_info(url: str) -> dict:
    """
    Extract basic information from YouTube URL.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        dict: Dictionary with video information
    """
    from transcript_extractor import extract_video_id
    
    video_id = extract_video_id(url)
    
    if not video_id:
        return {"error": "Invalid YouTube URL"}
    
    return {
        "video_id": video_id,
        "url": url,
        "embed_url": f"https://www.youtube.com/embed/{video_id}"
    }

def format_time(seconds: float) -> str:
    """
    Convert seconds to MM:SS format.
    
    Args:
        seconds (float): Time in seconds
        
    Returns:
        str: Formatted time string
    """
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
