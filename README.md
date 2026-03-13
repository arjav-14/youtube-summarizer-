# AI YouTube Video Summarizer

A powerful AI-powered YouTube video summarizer that works with both captioned and non-captioned videos. Uses Groq's Llama 3 model for intelligent summarization and OpenAI's Whisper for speech-to-text when captions aren't available.

## ✨ Features

- 🎥 **Dual Processing**: Works with both captioned and non-captioned YouTube videos
- 🤖 **AI-Powered**: Uses Groq's Llama 3 for intelligent summarization
- 🎤 **Speech-to-Text**: Automatically transcribes audio using Whisper when captions are unavailable
- 📱 **Modern UI**: Clean, responsive Streamlit interface
- ⚡ **Fast Processing**: Optimized chunking for long videos
- 💾 **Export Options**: Download transcripts and summaries
- 🔒 **Secure**: API key management with environment variable support

## 🏗️ Architecture

```
User enters YouTube URL
        ↓
Streamlit UI
        ↓
Extract Video ID
        ↓
Try caption extraction
        ↓
Caption available?
     /          \
   YES          NO
   ↓            ↓
youtube-transcript-api     Download audio (yt-dlp)
   ↓                        ↓
Transcript text             Whisper speech-to-text
           ↓
        Clean text
           ↓
       Chunk long text
           ↓
Send chunks to Groq (Llama 3)
           ↓
Generate summaries
           ↓
Combine summaries
           ↓
Display:
• Transcript
• AI summary
```

## 🛠️ Technologies Used

| Component | Tool |
|-----------|------|
| Frontend | Streamlit |
| Caption extraction | youtube-transcript-api |
| Audio download | yt-dlp |
| Speech-to-text | OpenAI Whisper |
| AI summarization | Groq |
| LLM | Llama 3 |

## 📋 Prerequisites

1. **Python 3.8+**
2. **FFmpeg** (required for audio processing)
3. **Groq API Key** (get one at [console.groq.com](https://console.groq.com/))

### Installing FFmpeg

#### Windows:
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add to PATH: `C:\ffmpeg\bin`

#### macOS:
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install ffmpeg
```

## 🚀 Setup and Installation

### 1. Clone or Download the Project
```bash
git clone <repository-url>
cd youtube_summarizer
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables (Optional)
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

Or set it in your system environment variables.

## 🎯 Usage

### Method 1: Run Directly
```bash
streamlit run app.py
```

### Method 2: Using the Web Interface
1. Open your browser and go to `http://localhost:8501`
2. Enter your Groq API key in the sidebar
3. Paste a YouTube video URL
4. Click "Generate Summary"
5. Wait for processing (may take a few minutes for long videos)

### Method 3: Using Python Scripts
You can also use the individual components programmatically:

```python
from transcript_extractor import extract_transcript, extract_video_id
from summarizer import GroqSummarizer

# Extract video ID
video_id = extract_video_id("https://www.youtube.com/watch?v=VIDEO_ID")

# Get transcript
transcript = extract_transcript(video_id)

# Summarize
summarizer = GroqSummarizer(api_key="your_api_key")
summary = summarizer.summarize_text(transcript)

print(summary)
```

## 📁 Project Structure

```
youtube_summarizer/
│
├── app.py                    # Main Streamlit application
├── transcript_extractor.py   # YouTube transcript extraction
├── audio_extractor.py        # Audio download functionality
├── speech_to_text.py         # Whisper speech-to-text
├── summarizer.py             # Groq summarization logic
├── utils.py                  # Utility functions
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## ⚙️ Configuration Options

### Whisper Models
- `tiny`: Fastest, least accurate (~32MB)
- `base`: Good balance (~142MB) - **Default**
- `small`: Better accuracy (~466MB)
- `medium`: High accuracy (~1.5GB)
- `large`: Best accuracy (~2.9GB)

### Text Chunking
- Default chunk size: 2000 characters
- Overlap: 100 characters between chunks
- Adjustable via the sidebar slider

## 🔧 Troubleshooting

### Common Issues

1. **FFmpeg not found**
   - Ensure FFmpeg is installed and in your PATH
   - Restart your terminal after installation

2. **API Key errors**
   - Verify your Groq API key is valid
   - Check if you have sufficient credits

3. **Video processing fails**
   - Check if the video is public and accessible
   - Verify your internet connection
   - Some videos may be region-restricted

4. **Memory issues with large models**
   - Use a smaller Whisper model (`base` or `tiny`)
   - Ensure you have sufficient RAM

### Performance Tips

1. **For faster processing**: Use the `base` Whisper model
2. **For better accuracy**: Use the `small` or `medium` Whisper model
3. **For very long videos**: Increase the chunk size in the sidebar

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Create an issue in the repository
3. Contact the project maintainer

---

**Note**: This tool is for educational and personal use. Please respect YouTube's terms of service and copyright laws when using this application.
