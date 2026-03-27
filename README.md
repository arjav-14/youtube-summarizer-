# AI YouTube Video Summarizer

A powerful AI-powered YouTube video summarizer that works with both captioned and non-captioned videos. Uses Groq's Llama 3 model for intelligent summarization and OpenAI's Whisper for speech-to-text when captions aren't available.

## 🧠 **Deep Learning Architecture**

### **Models Used**

#### **1. OpenAI Whisper (Speech-to-Text)**
- **Model Type**: Encoder-Decoder Transformer with Attention Mechanisms
- **Architecture**: 
  - **Encoder**: Processes audio spectrograms into contextual embeddings
  - **Decoder**: Generates text sequences from embeddings  
  - **Attention**: Weights importance of different audio segments
- **Training Data**: 680,000 hours of multilingual audio data
- **Model Variants**: tiny, base, small, medium, large (user selectable)
- **Why Whisper**: State-of-the-art accuracy, robust to noise, handles 99+ languages

#### **2. Meta Llama 3 (Text Summarization)**
- **Model Type**: Decoder-Only Transformer (70B parameters)
- **Architecture**:
  - **Context Window**: 8192 tokens for long-form content
  - **Instruction Following**: Fine-tuned for summarization tasks
  - **Optimized Inference**: Fast processing via Groq API
- **Why Llama 3**: Open-source transparency, superior reasoning, efficient for instruction-based tasks

### **Technical Implementation**
```python
# Whisper Integration (speech_to_text.py):
model = whisper.load_model(model_size, device=device)
result = model.transcribe(audio_file, fp16=False if device=="cpu" else True)

# Llama 3 Integration (summarizer.py):
client = Groq(api_key=api_key)
response = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[{"role": "user", "content": prompt}]
)
```

## 🔄 **Complete Project Flow**

### **Data Pipeline Architecture**
```
YouTube URL Input
        ↓
Video ID Extraction (transcript_extractor.py)
        ↓
Dual Path Selection:
┌─── Caption Available? ──→ YouTube Transcript API
│                      └─→ Text Processing
└─── No Captions? ──→ Audio Download (yt-dlp)
                       └─→ Format Conversion (FFmpeg)
                              └─→ Speech-to-Text (Whisper)
                                      └─→ Text Processing
                                             └─→ Text Chunking (2000 char segments)
                                                    └─→ AI Summarization (Llama 3 via Groq)
                                                           └─→ Summary Synthesis
                                                                  └─→ Final Output Display
```

### **Error Handling & Fallbacks**
```
Primary Path: Captions → Transcript → Chunking → Summarization
Fallback Path: Audio Download → FFmpeg → Whisper → Chunking → Summarization
Error Recovery: Multiple retry mechanisms with detailed logging
```

### **Processing Optimizations**
- **Chunking Strategy**: Overlapping segments (2000 chars, 100 overlap) for context preservation
- **Device Detection**: Auto CUDA/CPU selection for optimal performance
- **Format Flexibility**: MP3, WebM, M4A audio support
- **Path Resolution**: Cross-platform absolute path handling

## 🎯 **Why This Architecture?**

### **Academic Rationale**

#### **1. Modularity & Maintainability**
- **Separation of Concerns**: Audio processing isolated from text processing
- **Model Abstraction**: Easy to swap/update deep learning models
- **Error Isolation**: Independent failure handling for debugging
- **Code Organization**: Each model in dedicated module

#### **2. Scalability & Performance**
- **Horizontal Scaling**: Add more summarization models easily
- **Vertical Scaling**: Process arbitrarily long videos with intelligent chunking
- **Resource Management**: Memory-efficient processing for large files
- **GPU Optimization**: CUDA acceleration when available

#### **3. Robustness & Accessibility**
- **Multiple Input Formats**: Automatic caption/audio detection
- **Fallback Mechanisms**: Graceful degradation when primary path fails
- **Universal Support**: Works with any YouTube video
- **Comprehensive Testing**: Edge case handling and error recovery

### **Deep Learning Engineering Principles**
- **State-of-the-Art Models**: Leverages best available research models
- **Production-Ready**: Error handling, logging, and monitoring
- **User Experience**: Real-time feedback and progress tracking
- **Cross-Platform**: Windows, macOS, Linux compatibility

## 🚀 **Innovation Points**

### **Novel Contributions**
1. **Dual-Path Processing**: Intelligent caption/audio detection and selection
2. **Smart Chunking Algorithm**: Preserves semantic context across text segments
3. **Format-Agnostic Design**: Universal YouTube video processing
4. **Real-Time Progress Tracking**: Comprehensive user feedback system
5. **Hybrid Model Integration**: Combines speech recognition with language understanding

### **Research Implications**
- **Digital Accessibility**: Makes video content available to all users
- **Educational Technology**: Efficient learning from video content
- **Productivity Enhancement**: Quick information extraction and summarization
- **Multilingual Support**: Cross-language content processing
- **Cost Efficiency**: Optimized API usage and resource management

## ✨ Features

- 🎥 **Dual Processing**: Works with captions OR audio transcription
- 🤖 **AI-Powered**: Uses Groq's Llama 3 for intelligent summarization
- 🎤 **Speech-to-Text**: Automatic transcription using OpenAI's Whisper
- 📱 **Modern UI**: Clean, responsive Streamlit interface with dark theme
- ⚡ **Fast Processing**: Optimized chunking for long videos
- 💾 **Export Options**: Download transcripts and summaries
- 🔒 **Secure**: API key management with environment variable support

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   YouTube Video Summarizer              │
├─────────────────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────┐    ┌─────────────────┐    │
│  │   Streamlit    │    │   Groq Llama 3 │    │
│  │     UI         │    │  Summarization  │    │
│  └─────────────────┘    └─────────────────┘    │
│           │                   │    │              │
│  ┌─────────────────────────────────────────────┐    │
│  │     YouTube Video Processing System        │    │
│  │                                     │    │
│  │  ┌─────────┐    ┌──────────┐    │    │
│  │  │Captions│    │   Audio    │    │    │
│  │  │Available?│    │ Download  │    │    │
│  │  └─────┬──┘    └──────┬───┘    │    │
│  │         │              │              │    │
│  │  ┌──────▼──┐    ┌──────────▼──┐    │    │
│  │  │Transcript │    │   Whisper     │    │    │
│  │  │  API     │    │ Speech-to-Text│    │    │
│  │  └──────┬──┘    └──────────┬───┘    │    │
│  │         │              │              │    │
│  │  ┌─────────────────────────────────────┐    │
│  │  │     Text Processing Pipeline        │    │
│  │  │                                     │    │
│  │  │  ┌──────────┐    ┌──────────┐    │    │
│  │  │  │Chunking  │    │  AI Summary│    │    │
│  │  │  │Algorithm │    │  Generation │    │    │
│  │  │  └─────┬────┘    └─────┬────┘    │    │
│  │  │         │              │              │    │
│  │  └─────────────────────────────────────┘    │
│                                     │              │
├─────────────────────────────────────────────────────────┤
│                   Final Output Display              │
└─────────────────────────────────────────────────────────┘
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

## 🎓 **Educational Value**

### **Learning Objectives**
This project demonstrates practical application of cutting-edge deep learning technologies:

#### **Speech Recognition Technology**
- **Transformer Architecture**: Understanding attention mechanisms in sequence modeling
- **End-to-End Learning**: Direct audio-to-text mapping without intermediate steps
- **Multilingual Capability**: Processing diverse language content
- **Robustness**: Handling real-world audio challenges (noise, accents)

#### **Natural Language Processing**
- **Large Language Models**: Context understanding and generation
- **Summarization Techniques**: Extracting key information from long texts
- **Instruction Following**: AI model fine-tuning for specific tasks
- **Token Management**: Handling context windows for long-form content

#### **Software Engineering**
- **Modular Design**: Separating concerns for maintainability
- **Error Handling**: Robust fallback mechanisms and debugging
- **API Integration**: Working with external AI services
- **User Experience**: Real-time feedback and progress tracking

### **Technical Skills Demonstrated**
- **Deep Learning Model Integration**: Whisper + Llama 3 pipeline
- **Audio Processing**: Format conversion and optimization
- **Text Processing**: Chunking algorithms and context preservation
- **Web Development**: Streamlit for interactive applications
- **System Design**: Cross-platform compatibility and resource management

## 🚀 **Future Enhancements**

### **Potential Improvements**

#### **Model Upgrades**
- **Whisper-Large-v3**: Latest speech recognition improvements
- **Llama 3 Variants**: 8B, 405B for different use cases
- **Custom Models**: Fine-tuned models for specific domains
- **Multimodal Integration**: Video analysis alongside audio/text

#### **Feature Expansions**
- **Speaker Diarization**: Identifying different speakers in audio
- **Timestamp Alignment**: Synchronizing transcript with video timing
- **Language Detection**: Automatic source language identification
- **Quality Scoring**: Confidence metrics for transcription/summary quality
- **Batch Processing**: Multiple video processing capabilities

#### **Technical Enhancements**
- **Streaming Support**: Real-time transcription for live content
- **Caching System**: Model and result caching for efficiency
- **API Rate Limiting**: Intelligent request management
- **Database Integration**: Storing and retrieving past summaries
- **Mobile Optimization**: Responsive design for mobile devices

### **Research Applications**
- **Content Analysis**: Large-scale video dataset analysis
- **Educational Tools**: Study aid and lecture summarization
- **Accessibility Tools**: Making video content accessible to all
- **Productivity Applications**: Meeting transcription and summarization

---

**This project represents a comprehensive implementation of modern deep learning technologies for practical, real-world applications in speech recognition and natural language processing.** 🎓✨

## 🛠️ Technologies Used

| Component | Tool |
|-----------|------|
| Frontend | Streamlit |
| Caption extraction | youtube-transcript-api |
| Audio download | yt-dlp |
| Speech-to-text | OpenAI Whisper |
| AI summarization | Groq |
| LLM | Llama 3 |

## � **Deployment Guide**

### **Local Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
streamlit run app.py
```

### **Production Deployment**

#### **Option 1: Streamlit Cloud (Easiest)**
```bash
# Install Streamlit CLI
pip install streamlit

# Deploy to Streamlit Cloud
streamlit deploy

# Access your app
# https://your-app-name.streamlit.app
```

#### **Option 2: Railway**
```bash
# Create requirements.txt
echo "streamlit>=1.29.0" > requirements.txt
echo "youtube-transcript-api>=0.6.2" >> requirements.txt
echo "yt-dlp>=2023.12.30" >> requirements.txt
echo "groq>=0.4.1" >> requirements.txt
echo "openai-whisper>=20231117" >> requirements.txt
echo "torch>=2.1.0" >> requirements.txt
echo "ffmpeg-python>=0.2.0" >> requirements.txt

# Deploy to Railway
railway up
```

#### **Option 3: Heroku**
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# Create runtime.txt
echo "python-3.9.16" > runtime.txt

# Deploy to Heroku
heroku create your-app-name
heroku buildpacks:set heroku/python
git init
git add .
git commit -m "Deploy YouTube Summarizer"
heroku git:remote -a heroku https://git.heroku.com/your-app.git
git push heroku main
```

#### **Option 4: Docker**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

```bash
# Build and run
docker build -t youtube-summarizer .
docker run -p 8501:8501 youtube-summarizer
```

#### **Option 5: Self-Hosted VPS**
```bash
# Install dependencies
pip install -r requirements.txt

# Create systemd service
sudo tee /etc/systemd/system/youtube-summarizer.service > /dev/null <<EOF
[Unit]
Description=YouTube Video Summarizer
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/app
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port=8501
Restart=always
EOF

# Enable and start
sudo systemctl enable youtube-summarizer
sudo systemctl start youtube-summarizer
```

### **Environment Variables**
```bash
# Set Groq API key
export GROQ_API_KEY="your-api-key-here"

# Optional: Set custom model
export WHISPER_MODEL="base"  # tiny, small, medium, large
export CHUNK_SIZE="2000"  # Text chunk size
```

### **Security Considerations**
- **API Key Protection**: Never commit API keys to git
- **Input Validation**: Sanitize YouTube URLs and user inputs
- **Rate Limiting**: Implement API request throttling
- **HTTPS Only**: Use SSL certificates in production
- **User Authentication**: Add login system for multi-user access

### **Monitoring & Analytics**
```python
# Add logging
import logging
logging.basicConfig(level=logging.INFO)

# Add usage analytics
def track_usage(video_length, processing_time):
    print(f"Processed {video_length} seconds in {processing_time} seconds")
```

### **Scaling Considerations**
- **Horizontal Scaling**: Load balancers for multiple instances
- **Database**: PostgreSQL/MySQL for user data storage
- **CDN**: CloudFlare for static assets
- **Caching**: Redis for frequent requests
- **Background Jobs**: Celery for long-running tasks
**Your YouTube Video Summarizer is now ready for deployment to multiple platforms!** 🌐✨

##  Prerequisites

1. **Python 3.8+**
2. **FFmpeg** (required for audio processing)
3. **Groq API Key** (get one at [console.groq.com](https://console.groq.com/))
4. **Git** (for version control and deployment)

### Installing FFmpeg

#### Windows:
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg\bin`
3. Add to PATH: `setx PATH %PATH%;C:\ffmpeg\bin`

#### macOS:
```bash
brew install ffmpeg
```

#### Linux:
```bash
sudo apt update
sudo apt install ffmpeg
```

### Quick Start Commands
```bash
# Clone the repository
git clone https://github.com/yourusername/youtube-summarizer.git
cd youtube-summarizer

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GROQ_API_KEY="your-api-key-here"

# Run the application
streamlit run app.py
```

## 🚀 Setup and Installation

### 1. Clone or Download the Project
```bash
git clone <repository-url>
cd youtube_summarizer
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv youtube_summarizer_env

# Activate environment
# Windows:
youtube_summarizer_env\Scripts\activate
# macOS/Linux:
source youtube_summarizer_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GROQ_API_KEY="your-api-key-here"

# Run the application
streamlit run app.py
```
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import streamlit, whisper, groq; print('All dependencies installed successfully!')"
```

### 4. Configure Environment Variables
```bash
# Set Groq API key (required)
export GROQ_API_KEY="your-api-key-here"

# Optional: Set custom preferences
export WHISPER_MODEL="base"  # tiny, small, medium, large
export CHUNK_SIZE="2000"  # Text chunk size
export MAX_VIDEO_LENGTH="3600"  # Max video length (seconds)
```

### 5. Run Application
```bash
# Start the Streamlit app
streamlit run app.py

# Access at: http://localhost:8501
```

## 🎯 **Troubleshooting**

### **Common Issues**

#### **FFmpeg Not Found**
```bash
# Check if FFmpeg is installed
ffmpeg -version

# Add to PATH (Windows)
set PATH=%PATH%;C:\ffmpeg\bin

# Install with package manager
pip install ffmpeg-python
```

#### **Model Not Available**
```bash
# Check Groq model availability
curl -H "Authorization: Bearer $GROQ_API_KEY" \
     https://api.groq.com/openai/v1/models

# Update model in summarizer.py
# Change to: "llama3-8b-8192" → "llama3-70b-8192"
```

#### **Memory Issues with Large Videos**
```bash
# Use smaller Whisper model
export WHISPER_MODEL="tiny"

# Reduce chunk size
export CHUNK_SIZE="1000"

# Enable CPU-only mode
export FORCE_CPU="true"
```

#### **API Rate Limits**
```python
# Add rate limiting in summarizer.py
import time
import random

def rate_limited_request():
    time.sleep(random.uniform(1, 3))  # Random delay
```

---

## 📞 **Support & Contributing**

### **Getting Help**
- **Documentation**: Check README.md for detailed guides
- **Issues**: Report bugs at [GitHub Issues](link-to-issues)
- **Features**: Request enhancements via [GitHub Discussions](link-to-discussions)

### **Contributing Guidelines**
1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature-name`
3. **Make changes**: Test thoroughly
4. **Submit PR**: With clear description and tests
5. **Follow code style**: PEP 8 and existing patterns

### **Development Setup**
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black *.py
flake8 *.py
```

---

**🎉 Your YouTube Video Summarizer is now ready for development, deployment, and collaboration!**
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables (Optional)
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

Or set it in your system environment variables.

#### **Using .env file (Recommended)**
Create a `.env` file in the project root:
```bash
# Create .env file
cat > .env <<EOF
GROQ_API_KEY=your_groq_api_key_here
WHISPER_MODEL=base
CHUNK_SIZE=2000
MAX_VIDEO_LENGTH=3600
EOF

# Load in Python
from dotenv import load_dotenv
load_dotenv()  # Automatically loads .env file
```

**Security Note**: Never commit `.env` file to version control! Add to `.gitignore`:
```gitignore
.env
*.pyc
__pycache__/
audio.*
```

---

**🎉 Your YouTube Video Summarizer is now ready for development, deployment, and collaboration!**

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
5. Wait for processing to complete
6. View your transcript and AI summary

### Method 3: Using API (Advanced)
```python
# Example script to use the summarizer programmatically
from summarizer import GroqSummarizer

# Extract video ID
video_id = extract_video_id("https://www.youtube.com/watch?v=VIDEO_ID")

# Get transcript
transcript = extract_transcript(video_id)

# Initialize summarizer
summarizer = GroqSummarizer(api_key="your_api_key")

# Extract video ID
video_id = extract_video_id("https://www.youtube.com/watch?v=VIDEO_ID")

# Get transcript
transcript = extract_transcript(video_id)

# Summarize
summary = summarizer.summarize_text(transcript)
print(f"Summary: {summary}")
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
