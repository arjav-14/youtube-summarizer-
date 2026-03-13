
import os


# Force add FFmpeg path
os.environ["PATH"] += os.pathsep + r"C:\Users\arjav\OneDrive\Desktop\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin"
import whisper
import torch
import shutil
import stat

def convert_audio_to_text(file_path, model_size="base"):
    """
    Convert audio file to text using Whisper.
    
    Args:
        file_path (str): Path to audio file
        model_size (str): Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
        
    Returns:
        str: Transcribed text or None if failed
    """
    try:
        print(f"Speech to text - Input file path: {file_path}")
        
        # Check if file exists
        abs_path = os.path.abspath(file_path)
        print(f"Speech to text - Absolute path: {abs_path}")
        print(f"Speech to text - Current working directory: {os.getcwd()}")
        
        if not os.path.exists(abs_path):
            print(f"Audio file not found: {abs_path}")
            return None
        
        print(f"File permissions: {oct(os.stat(abs_path).st_mode)[-3:]}")
        print(f"File size: {os.path.getsize(abs_path)} bytes")
        print(f"Using absolute path: {abs_path}")
        
        # Check if CUDA is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        # Load Whisper model
        print(f"Loading Whisper model: {model_size}")
        model = whisper.load_model(model_size, device=device)
        
        # Transcribe audio
        print(f"Transcribing audio file: {abs_path}")
        result = model.transcribe(abs_path, fp16=False if device == "cpu" else True)
        
        return result["text"]

    except Exception as e:
        print("Whisper error:", e)
        return None

def find_ffmpeg():
    """
    Find FFmpeg executable location.
    
    Returns:
        str: Path to FFmpeg directory or None if not found
    """
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

def check_whisper_model_exists(model_size="base"):
    """
    Check if Whisper model is already downloaded.
    
    Args:
        model_size (str): Whisper model size
        
    Returns:
        bool: True if model exists, False otherwise
    """
    try:
        whisper.load_model(model_size)
        return True
    except Exception:
        return False
