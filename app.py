"""
================================================================================
COMMUNITY ENGINE: STREAMLIT MISSION-DRIVEN VIDEO HUB & AUTOMATED CALENDAR
================================================================================
Role: Principal Software Engineer & AI Solutions Architect
Target Client: Collaborative Center for Social Innovation (CCSI), Buffalo, NY

Required Dependencies:
pip install streamlit openai-whisper google-genai moviepy pydantic pandas

External System Dependencies:
- FFmpeg must be installed and accessible on your system's environmental PATH.

Required Environment Variables:
- GEMINI_API_KEY: Must be set with a valid Google Gemini API Key.
================================================================================
"""

import os
import json
import csv
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

# Frontend and System Frameworks
import streamlit as st
import pandas as pd
import whisper
from google import genai
from google.genai import types
from moviepy.editor import VideoFileClip

# Set up beautiful web page configuration
st.set_page_config(page_title="CCSI CommUNITY Engine", page_icon="🌱", layout="wide")

# ================================================================================
# PYDANTIC DEFINITIONS FOR STRICT MISSION-ALIGNED STRUCTURED OUTPUT
# ================================================================================
class HighlightSegment(BaseModel):
    start_time: float = Field(..., description="The start timestamp of the clip in seconds.")
    end_time: float = Field(..., description="The end timestamp of the clip in seconds.")
    content_pillar: str = Field(..., description="Must explicitly map to one of CCSI's 5 pillars.")
    suggested_hook: str = Field(..., description="A compelling, warm, reflective social headline and descriptive caption honoring CCSI guidelines. No sensationalist clickbait.")
    defensibility_note: str = Field(..., description="A clear, 1-sentence defense explaining to a board member or funder exactly why this moment aligns with CCSI's mission.")

class HighlightAnalysisResponse(BaseModel):
    clips: List[HighlightSegment] = Field(..., description="Array containing exactly the top 5 highly mission-aligned short form clips.")

# ================================================================================
# PIPELINE FUNCTIONS
# ================================================================================

def transcribe_video(video_path: str) -> List[Dict]:
    """Transcribes the video audio using OpenAI's Whisper model."""
    try:
        model = whisper.load_model("base")
        result = model.transcribe(video_path, verbose=False)
        structured_segments = []
        for segment in result.get("segments", []):
            structured_segments.append({
                "start": round(float(segment["start"]), 2),
                "end": round(float(segment["end"]), 2),
                "text": segment["text"].strip()
            })
        return structured_segments
    except Exception as e:
        st.error(f"Transcription failed: {str(e)}")
        raise e

def analyze_highlights_with_gemini(transcript_segments: List[Dict]) -> List[Dict]:
    """Uses Gemini 2.5 Flash to pick mission-aligned, collective-community moments."""
    client = genai.Client()
    serialized_transcript = ""
    for seg in transcript_segments:
        serialized_transcript += f"[{seg['start']} - {seg['end']}] {seg['text']}\n"

    system_instruction = (
        "You are an elite AI Solutions Architect embedded within the Collaborative Center for Social Innovation (CCSI).\n"
        "Your task is to isolate exactly 5 short-form clips from the transcript that strictly advance our mission.\n"
        "Each clip must be under 30 seconds in duration.\n\n"
        "CRITICAL BRAND FILTERS:\n"
        "1. NO CLICKBAIT REACH: Do not choose superficial, loud, or performative moments.\n"
        "2. COLLABORATIVE PRONOUNS: Prioritize sequences using 'We', 'Our team', 'Our neighborhood', or 'Our community' instead of 'I' or 'Me'.\n"
        "3. STRUCTURAL AGENCY SHIFTS: Highlight transitions where a youth speaker shifts from passive language stating a problem to active solution-oriented leadership.\n"
        "4. ABSOLUTE GUARDRAILS: Reject any segments utilizing deficit-based framing ('at-risk kids', 'saving students') or founder-as-hero framing.\n"
        "5. PILLAR ASSIGNMENT: Map each clip explicitly to one of CCSI's 5 official Content Pillars."
    )

    prompt = f"Analyze this transcript timeline and select exactly 5 clips (under 30s each):\n\n{serialized_transcript}"

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.15,
                response_mime_type="application/json",
                response_schema=HighlightAnalysisResponse,
            ),
        )
        return json.loads(response.text).get("clips", [])
    except Exception as e:
        st.error(f"Gemini Analysis failed: {str(e)}")
        raise e

def clip_and_crop_video(video_path: str, highlights: List[Dict], output_dir: str = "output_shorts") -> List[str]:
    """Slices and converts horizontal widescreen 16:9 videos into center-cropped vertical 9:16 clips."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generated_filenames = []
    try:
        master_clip = VideoFileClip(video_path)
        orig_w, orig_h = master_clip.size
        target_w = int((orig_h * 9) / 16)
        x1 = int((orig_w - target_w) / 2)
        x2 = x1 + target_w

        for index, clip_data in enumerate(highlights):
            start = clip_data.get("start_time")
            end = clip_data.get("end_time")
            if (end - start) > 30.0:
                end = start + 30.0
                
            output_filename = f"ccsi_short_{index+1}.mp4"
            output_filepath = os.path.join(output_dir, output_filename)
            
            sliced_clip = master_clip.subclip(start, end)
            cropped_clip = sliced_clip.crop(x1=x1, y1=0, x2=x2, y2=orig_h)
            
            cropped_clip.write_videofile(
                output_filepath, codec="libx264", audio_codec="aac", preset="ultrafast", bitrate="2000k", logger=None
            )
            generated_filenames.append(output_filepath)
            
        master_clip.close()
        return generated_filenames
    except Exception as e:
        st.error(f"Video editing failed: {str(e)}")
        raise e

# ================================================================================
# STREAMLIT USER INTERFACE LAYOUT
# ================================================================================

st.title("🌱 CCSI CommUNITY Engine")
st.subheader("Transforming Long-Form Footage into Mission-Driven, Funder-Credible Content Calendar Assets")

# Sidebar setup for developer options & API validation
st.sidebar.header("System Settings")
api_key_input = st.sidebar.text_input("Gemini API Key", value=os.environ.get("GEMINI_API_KEY", ""), type="password")
if api_key_input:
    os.environ["GEMINI_API_KEY"] = api_key_input

st.sidebar.markdown("""
### **How it Works (The Magic Folder Setup)**
This dashboard acts as the command center. In full deployment, it monitors a **Google Drive** folder. The moment a workshop or pitch day video finishes uploading, this app wakes up automatically.
""")

# Main Content Dashboard Split Window
uploaded_file = st.file_uploader("Upload Long-Form Video Asset (MP4 format)", type=["mp4"])

if uploaded_file:
    # Save the uploaded file temporarily to the local disk space
    temp_video_path = f"temp_master_{uploaded_file.name}"
    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.read())
        
    st.video(temp_video_path, start_time=0)
    
    if st.button("🚀 Process Video & Generate Content Calendar"):
        if not os.environ.get("GEMINI_API_KEY"):
            st.error("Please enter a valid Gemini API Key in the sidebar configuration container.")
        else:
            with st.spinner("Step 1 of 3: Transcribing audio with local Whisper engine..."):
                transcript = transcribe_video(temp_video_path)
                
            with st.spinner("Step 2 of 3: Evaluating collective metrics & guardrails with Gemini 2.5 Flash..."):
                highlights = analyze_highlights_with_gemini(transcript)
                
            with st.spinner("Step 3 of 3: Cutting and cropping center-focused 9:16 mobile shorts..."):
                clip_paths = clip_and_crop_video(temp_video_path, highlights)
                
            st.success("🎉 Marketing Pipeline Completed Successfully!")
            
            # --- RENDER CALENDAR RESULTS TAB ---
            st.header("🗓️ Automated Content Calendar")
            
            calendar_rows = []
            current_date = datetime.now()
            
            for index, clip_data in enumerate(highlights):
                post_date = (current_date + timedelta(days=index * 7)).strftime("%B %d, %Y")
                calendar_rows.append({
                    "Post Date": post_date,
                    "Target File": f"ccsi_short_{index+1}.mp4",
                    "Assigned Pillar": clip_data.get("content_pillar"),
                    "Suggested Caption / Hook": clip_data.get("suggested_hook"),
                    "Funder Defensibility (Why We Chose This)": clip_data.get("defensibility_note")
                })
                
            df = pd.DataFrame(calendar_rows)
            st.dataframe(df, use_container_width=True)
            
            # Allow downloading the CSV directly
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Calendar CSV (Ready to Import into Buffer/Hootsuite)",
                data=csv_data,
                file_name="ccsi_content_schedule.csv",
                mime="text/csv"
            )
            
            # --- RENDER EXPORTED SHORT CLIPS IN GRID ---
            st.header("📱 Extracted Mobile-Ready Shorts Preview")
            cols = st.columns(len(clip_paths))
            for index, path in enumerate(clip_paths):
                with cols[index]:
                    st.subheader(f"Short #{index+1}")
                    st.video(path)
                    st.caption(f"**Pillar:** {calendar_rows[index]['Assigned Pillar']}")
                    
            # Cleanup temporary master file asset
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
