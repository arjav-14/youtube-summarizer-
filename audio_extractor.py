import yt_dlp
import os
import tempfile
import shutil

# Add FFmpeg to PATH from user's installation
ffmpeg_path = r"C:\Users\arjav\OneDrive\Desktop\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin"
if os.path.exists(ffmpeg_path):
    os.environ["PATH"] += os.pathsep + ffmpeg_path
    print(f"Added FFmpeg to PATH: {ffmpeg_path}")
else:
    print(f"FFmpeg not found at: {ffmpeg_path}")

def download_audio(url, output_path="audio"):
    """
    Download audio from YouTube video.
    
    Args:
        url (str): YouTube video URL
        output_path (str): Output file path (without extension)
        
    Returns:
        str: Path to downloaded audio file or None if failed
    """
    # Download audio with FFmpeg postprocessing for MP3 conversion
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': False,
    }

    try:
        print(f"Current working directory: {os.getcwd()}")
        print(f"Looking for files with pattern: {output_path}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("Download completed. Checking files...")
        
        # List all files in current directory
        all_files = os.listdir('.')
        print(f"All files in directory: {all_files}")
        
        # Check for different possible extensions
        possible_files = [
            f"{output_path}.mp3",
            f"{output_path}.webm", 
            f"{output_path}.m4a"
        ]
        
        for file_path in possible_files:
            abs_path = os.path.abspath(file_path)
            print(f"Checking for file: {abs_path}")
            print(f"File exists: {os.path.exists(abs_path)}")
            if os.path.exists(abs_path):
                print(f"Found audio file: {abs_path}")
                print(f"File size: {os.path.getsize(abs_path)} bytes")
                return abs_path
        
        print("No audio file found after download")
        return None

    except Exception as e:
        print("Download error:", e)
        return None

def find_ffmpeg():
    """
    Find FFmpeg executable location.
    
    Returns:
        str: Path to FFmpeg directory or None if not found
    """
    # Try your FFmpeg source location first
    ffmpeg_source_path = r"C:\Users\arjav\OneDrive\Desktop"
    if os.path.exists(os.path.join(ffmpeg_source_path, "ffmpeg.exe")):
        return ffmpeg_source_path
    
    # Try common FFmpeg locations
    possible_paths = [
        r"C:\Program Files\ffmpeg\bin",
        r"C:\Program Files (x86)\ffmpeg\bin", 
        r"C:\ffmpeg\bin",
        os.path.expanduser(r"~\AppData\Local\Microsoft\WindowsApps"),
    ]
    
    # Check if ffmpeg is in PATH
    ffmpeg_in_path = shutil.which("ffmpeg")
    if ffmpeg_in_path:
        return os.path.dirname(ffmpeg_in_path)
    
    # Check common installation paths
    for path in possible_paths:
        if os.path.exists(os.path.join(path, "ffmpeg.exe")):
            return path
    
    return None

def cleanup_audio(file_path):
    """
    Clean up downloaded audio file.
    
    Args:
        file_path (str): Path to audio file to delete
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error cleaning up audio file: {e}")
