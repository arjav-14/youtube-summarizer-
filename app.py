import streamlit as st
import os
import time
from transcript_extractor import extract_transcript, extract_video_id
from audio_extractor import download_audio, cleanup_audio
from speech_to_text import convert_audio_to_text
from summarizer import GroqSummarizer
from utils import split_text, clean_transcript, extract_video_info


st.set_page_config(
    page_title="AI YouTube Video Summarizer",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme with white text
st.markdown("""
<style>
    /* Dark theme with white text */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #ffffff;
        margin-bottom: 2rem;
    }
    
    /* Message styling with dark backgrounds */
    .success-message {
        background-color: #1a1a1a;
        color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #28a745;
    }
    
    .warning-message {
        background-color: #1a1a1a;
        color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ffc107;
    }
    
    .error-message {
        background-color: #1a1a1a;
        color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dc3545;
    }
    
    /* Text input and button styling */
    .stTextInput > div > div > input,
    .stTextArea > div > textarea {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #404040;
    }
    
    .stButton > button {
        background-color: #007bff;
        color: #ffffff;
        border: none;
    }
    
    .stButton > button:hover {
        background-color: #0056b3;
        color: #ffffff;
    }
    
    /* Sidebar styling */
    .css-1lqqmzp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    /* Streamlit containers */
    .stApp > div {
        background-color: #000000;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-header">🎥 AI YouTube Video Summarizer</div>', unsafe_allow_html=True)
    
   
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # API Key input
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Enter your Groq API key. Get one at https://console.groq.com/",
            value=os.getenv("GROQ_API_KEY", "")
        )
        
        st.markdown("---")
        
        # Model selection
        model_size = st.selectbox(
            "Whisper Model Size",
            ["base", "small", "medium", "large"],
            index=0,
            help="Larger models are more accurate but slower and use more memory"
        )
        
        # Chunk size for long videos
        chunk_size = st.slider(
            "Text Chunk Size",
            min_value=1000,
            max_value=4000,
            value=2000,
            step=500,
            help="Size of text chunks for processing long videos"
        )
        
        st.markdown("---")
        
        # Instructions
        st.markdown("""
        ### 📋 Instructions:
        1. Enter your Groq API key
        2. Paste a YouTube URL
        3. Click "Generate Summary"
        4. Wait for processing
        
        ### 🔧 Requirements:
        - FFmpeg must be installed
        - Stable internet connection
        - Sufficient disk space for audio files
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("📹 Input")
        
        # URL input
        url = st.text_input(
            "YouTube Video URL",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Enter the full YouTube video URL"
        )
        
        # Process button
        if st.button("🚀 Generate Summary", type="primary", disabled=not (url and api_key)):
            process_video(url, api_key, model_size, chunk_size)
        
        # Sample URLs for testing
        st.markdown("---")
        st.markdown("### 🧪 Sample URLs:")
        sample_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Short video
            "https://www.youtube.com/watch?v=J_GJeY9lGgM",  # Educational content
        ]
        
        for sample_url in sample_urls:
            if st.button(f"Use Sample: {sample_url.split('=')[-1]}", key=f"sample_{sample_url.split('=')[-1]}"):
                st.session_state.sample_url = sample_url
        
        # Use sample URL if selected
        if 'sample_url' in st.session_state:
            url = st.session_state.sample_url
            st.text_input("YouTube Video URL", value=url, key="url_display")
    
    with col2:
        st.header("📊 Results")
        
        # Display results if available
        if 'results' in st.session_state:
            display_results()

def process_video(url, api_key, model_size, chunk_size):
    """Process the YouTube video and generate summary."""
    
    # Validate URL
    video_info = extract_video_info(url)
    if 'error' in video_info:
        st.error(f"❌ {video_info['error']}")
        return
    
    video_id = video_info['video_id']
    
    # Initialize progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Extract transcript
        status_text.text("🔍 Extracting transcript...")
        progress_bar.progress(10)
        
        # Step 1: Extract transcript (prioritize captions for Streamlit Cloud)
        status_text.text("🔍 Checking for captions...")
        progress_bar.progress(10)
        
        transcript = extract_transcript(video_id)
        
        if transcript:
            status_text.text("✅ Captions found! Processing transcript...")
            progress_bar.progress(30)
            transcript_method = "captions"
            st.success("🎉 Perfect! This video has captions available for processing.")
        else:
            # No captions available - try audio processing with user choice
            st.warning("🔇 No captions found for this video.")
            
            # Give user choice
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🎤 Try Audio Processing", help="Attempt to download and transcribe audio"):
                    st.session_state.audio_processing = True
                    status_text.text("⬇️ Downloading audio...")
                    progress_bar.progress(20)
                    
                    audio_file = download_audio(url)
                    
                    print("Audio file:", audio_file)
                    print("File exists:", os.path.exists(audio_file) if audio_file else "No file returned")
                    
                    if audio_file:
                        status_text.text("🎤 Transcribing audio...")
                        progress_bar.progress(40)
                        transcript = convert_audio_to_text(audio_file, model_size)
                        cleanup_audio(audio_file)  # Clean up audio file
                        
                        if transcript:
                            status_text.text("✅ Audio transcribed successfully!")
                            progress_bar.progress(50)
                            transcript_method = "whisper"
                            st.success("🎉 Audio processing completed!")
                        else:
                            st.error("❌ Failed to transcribe audio. Streamlit Cloud has restrictions on audio downloads.")
                            st.info("💡 **Alternative Solutions:**")
                            st.info("- 🌐 Deploy to Railway for better audio support")
                            st.info("- 🏠 Run locally (no restrictions)")
                            st.info("- 📚 Try videos with captions instead")
                            return
                    else:
                        st.error("❌ Failed to download audio due to Streamlit Cloud restrictions.")
                        st.info("💡 **Why this happens:** Streamlit Cloud limits network downloads for security.")
                        return
            
            with col2:
                if st.button("📚 Try Another Video", help="Choose a video with captions"):
                    st.info("🎯 **Videos with captions work best on Streamlit Cloud:**")
                    st.info("- 📚 Educational content (Khan Academy, MIT)")
                    st.info("- 📰 News videos (BBC, CNN)")
                    st.info("- 🎓 University lectures")
                    st.info("- 📺 Documentaries")
                    return
            
            # If user hasn't made a choice, show helpful info
            st.markdown("---")
            st.markdown("### 🎯 **Streamlit Cloud Tips:**")
            st.markdown("- 📚 **Captioned videos** work reliably")
            st.markdown("- 🎤 **Audio processing** may fail due to restrictions")
            st.markdown("- 🌐 **Alternative platforms** like Railway support audio better")
            
            st.markdown("### � **Test with these captioned videos:**")
            st.markdown("- https://www.youtube.com/watch?v=jNQXAC9IVRw (First YouTube video)")
            st.markdown("- https://www.youtube.com/watch?v=J_GJeY9lGgM (Khan Academy)")
            st.markdown("- https://www.youtube.com/watch?v=dQw4w9WgXcQ (Educational)")
            
            return
        
        # Clean transcript
        transcript = clean_transcript(transcript)
        
        # Step 4: Split text into chunks if needed
        status_text.text("📝 Processing transcript...")
        progress_bar.progress(60)
        
        chunks = split_text(transcript, chunk_size=chunk_size)
        
        # Step 5: Generate summary
        status_text.text("🤖 Generating summary...")
        progress_bar.progress(70)
        
        summarizer = GroqSummarizer(api_key=api_key)
        summary = summarizer.summarize_chunks(chunks, combine_summaries=True)
        
        progress_bar.progress(100)
        status_text.text("✅ Complete!")
        
        # Store results in session state
        st.session_state.results = {
            'video_info': video_info,
            'transcript': transcript,
            'summary': summary,
            'method': transcript_method,
            'chunks_count': len(chunks),
            'transcript_length': len(transcript)
        }
        
        # Success message
        st.success("🎉 Summary generated successfully!")
        
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        progress_bar.empty()
        status_text.empty()

def display_results():
    """Display the processing results."""
    
    results = st.session_state.results
    
    # Video information
    st.markdown("### 📹 Video Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Method Used", results['method'].title())
    
    with col2:
        st.metric("Chunks Processed", results['chunks_count'])
    
    with col3:
        st.metric("Transcript Length", f"{results['transcript_length']:,} chars")
    
    # Embed video
    st.markdown("### 🎥 Video Preview")
    st.markdown(f'<iframe width="100%" height="315" src="{results["video_info"]["embed_url"]}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
    
    # Summary section
    st.markdown("### 📋 AI Summary")
    st.markdown('<div class="success-message">' + results['summary'] + '</div>', unsafe_allow_html=True)
    
    # Transcript section (collapsible)
    with st.expander("📄 Full Transcript", expanded=False):
        st.text_area(
            "Complete Transcript",
            value=results['transcript'],
            height=400,
            disabled=True,
            help="The full transcript extracted from the video"
        )
        
        # Download transcript button
        if st.button("📥 Download Transcript"):
            st.download_button(
                label="Download as TXT",
                data=results['transcript'],
                file_name=f"transcript_{results['video_info']['video_id']}.txt",
                mime="text/plain"
            )
    
    # Download summary button
    st.markdown("### 💾 Export Options")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download Summary"):
            st.download_button(
                label="Download Summary as TXT",
                data=results['summary'],
                file_name=f"summary_{results['video_info']['video_id']}.txt",
                mime="text/plain"
            )
    
    with col2:
        if st.button("🔄 Process Another Video"):
            del st.session_state.results
            st.rerun()

if __name__ == "__main__":
    main()


