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
    # Download audio with Streamlit Cloud compatible settings
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
        'no_check_certificate': True,  # Skip SSL verification for Streamlit Cloud
        'socket_timeout': 60,  # Increase timeout
        'retries': 3,  # Retry failed downloads
    }

    try:
        # Use temporary directory for Streamlit Cloud
        import tempfile
        temp_dir = tempfile.mkdtemp()
        print(f"Using temporary directory: {temp_dir}")
        
        # Update output path to use temp directory
        temp_output_path = os.path.join(temp_dir, output_path)
        ydl_opts['outtmpl'] = os.path.join(temp_dir, f'{output_path}.%(ext)s')
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("Download completed. Checking files...")
        
        # List all files in temp directory
        all_files = os.listdir(temp_dir)
        print(f"All files in temp directory: {all_files}")
        
        # Check for different possible extensions
        possible_files = [
            os.path.join(temp_dir, f"{output_path}.mp3"),
            os.path.join(temp_dir, f"{output_path}.webm"), 
            os.path.join(temp_dir, f"{output_path}.m4a")
        ]
        
        for file_path in possible_files:
            if os.path.exists(file_path):
                print(f"Found audio file: {file_path}")
                print(f"File size: {os.path.getsize(file_path)} bytes")
                return file_path
        
        print("No audio file found after download")
        return None

    except Exception as e:
        print("Download error:", e)
        # Try alternative approach - direct webm download
        try:
            print("Trying alternative approach...")
            ydl_opts_alt = {
                'format': 'bestaudio[ext=webm]/bestaudio/best',
                'outtmpl': os.path.join(temp_dir, f'{output_path}.webm'),
                'quiet': False,
                'no_warnings': False,
                'no_check_certificate': True,
                'socket_timeout': 60,
                'retries': 3,
                'postprocessors': [],  # No postprocessing
            }
            
            with yt_dlp.YoutubeDL(ydl_opts_alt) as ydl:
                ydl.download([url])
            
            webm_file = os.path.join(temp_dir, f"{output_path}.webm")
            if os.path.exists(webm_file):
                print(f"Found webm file: {webm_file}")
                return webm_file
                
        except Exception as e2:
            print("Alternative approach also failed:", e2)
            
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
