from groq import Groq
import os
from typing import List, Optional

class GroqSummarizer:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq client for summarization.
        
        Args:
            api_key (str): Groq API key. If None, will try to get from environment
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable or pass api_key parameter.")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"  # Updated to supported model
    
    def summarize_text(self, text: str, max_length: int = 500) -> str:
        """
        Summarize a single chunk of text.
        
        Args:
            text (str): Text to summarize
            max_length (int): Maximum length of summary
            
        Returns:
            str: Summary text
        """
        prompt = f"""
Please summarize the following YouTube transcript chunk. Create a concise, informative summary that captures the main points and key information.

Guidelines:
- Keep the summary under {max_length} words
- Focus on the most important concepts and information
- Maintain the original meaning and context
- Use clear, readable language
- Include any important technical terms or concepts mentioned

Transcript:
{text}

Summary:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at summarizing educational and informational content from YouTube videos. Create clear, concise summaries that capture the essential information."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=800,
                top_p=1,
                stream=False
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"Error generating summary: {str(e)}"
    
    def summarize_chunks(self, chunks: List[str], combine_summaries: bool = True) -> str:
        """
        Summarize multiple text chunks.
        
        Args:
            chunks (List[str]): List of text chunks to summarize
            combine_summaries (bool): Whether to combine individual summaries into a final summary
            
        Returns:
            str: Final summary
        """
        if not chunks:
            return "No content to summarize."
        
        # Generate summaries for each chunk
        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            print(f"Summarizing chunk {i+1}/{len(chunks)}...")
            summary = self.summarize_text(chunk)
            chunk_summaries.append(summary)
        
        if not combine_summaries or len(chunk_summaries) == 1:
            return "\n\n".join(chunk_summaries)
        
        # Combine all summaries into a final summary
        combined_text = "\n\n".join(chunk_summaries)
        
        final_prompt = f"""
Please combine these partial summaries from a YouTube video into a comprehensive, well-structured final summary. The summaries cover different parts of the video in sequence.

Guidelines:
- Create a coherent narrative that flows logically
- Remove any redundancy between sections
- Highlight the most important concepts and takeaways
- Organize the information in a clear, easy-to-follow structure
- Keep the final summary comprehensive but concise
- Include any key insights or conclusions from the video

Partial summaries:
{combined_text}

Final comprehensive summary:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at creating comprehensive summaries from multiple partial summaries. Combine the information into a coherent, well-structured final summary."
                    },
                    {
                        "role": "user",
                        "content": final_prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000,
                top_p=1,
                stream=False
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating final summary: {e}")
            return "\n\n".join(chunk_summaries)  # Return combined summaries if final summarization fails

# Convenience function for backward compatibility
def summarize_text(text: str, api_key: Optional[str] = None) -> str:
    """
    Convenience function to summarize text using Groq.
    
    Args:
        text (str): Text to summarize
        api_key (str): Groq API key
        
    Returns:
        str: Summary text
    """
    summarizer = GroqSummarizer(api_key=api_key)
    return summarizer.summarize_text(text)
