# 🌱 CCSI CommUNITY Engine

### Transforming Long-Form Event Footage into Mission-Driven, Funder-Credible Social Presence Assets

The **CommUNITY Engine** is an automated, AI-powered system designed specifically for the **Collaborative Center for Social Innovation (CCSI)** in Buffalo, NY. It bridges the gap between massive long-form media files sitting unused in cloud storage and a consistent, high-impact social media presence that builds funder confidence, recruits entrepreneurs, and earns community trust over WNY.

---

## 📋 Challenge & Solution Context (End-User Focus)

### The Problem
CCSI produces hours of recorded panels, workshop sessions, and demo-day presentations. However, a lean staff carrying program delivery, fundraising, and communications cannot manually review hours of footage every week. Furthermore, traditional clip-cutting software optimizes purely for viral reach, which leads to clickbait rather than mission-relevant moments that make funders trust an organization's outcomes.

### Our Solution
The CommUNITY Engine provides a **repeatable, zero-touch pipeline** that strips out human labor and enforces absolute brand guardrails. It doesn't pick moments based on "hype." Instead, it uses advanced AI models to filter for collective community impact, youth leadership agency, and strict adherence to CCSI's 5 official Content Pillars.

---

## 🛠️ Technology Stack & Feasibility

This system uses entirely open-source and highly accessible technologies to ensure a realistic path for a lean nonprofit to maintain:

* **Frontend User Interface:** Streamlit (Hosted on the free Community Cloud)
* **Audio Transcription:** OpenAI Whisper ("base" execution model)
* **AI Evaluation & Guardrails:** Google Gemini 2.5 Flash
* **Video Processing Pipeline:** MoviePy (with FFmpeg spatial center-cropping transformations)
* **Data Serialization:** Pydantic & Pandas

---

## 🚀 How the System Functions End-to-End
[ Raw Video Upload ] ➡️ [ OpenAI Whisper ] ➡️ [ Gemini 2.5 Flash ] ➡️ [ MoviePy Engine ] ➡️ [ Final Deliverables ]
(Staff drops MP4)      (Auto-Transcription)   (Brand Filter Check)     (9:16 Center Crop)    (CSV Calendar + Clips)


1.  **Ingestion:** A non-technical staff member uploads a raw event recording (`.mp4`) into the dashboard.
2.  **Transcription:** OpenAI’s Whisper model processes the audio stream, outputting micro-timestamped text blocks.
3.  **AI Evaluation:** The transcript dataset is passed to Gemini 2.5 Flash using strict structured JSON schemas. The AI weights moments utilizing collaborative pronouns ("We", "Our community") over individualistic ones ("I", "Me") and flags systemic shifts where a speaker transitions from passive problem-stating to active leadership. Deficit-based language ("at-risk kids") is rejected automatically.
4.  **Automated Slicing & Geometric Cropping:** MoviePy extracts the exact timestamps chosen by the AI and executes non-destructive spatial trimming, converting horizontal 16:9 widescreen pixels into a mobile-centric vertical 9:16 aspect ratio.
5.  **Output Generation:** The system renders the final video files and builds a production-ready `.csv` content calendar.

---

## 🧑‍💻 User Operating Guide

Running the pipeline is designed to be dead-simple for non-technical CCSI staff:

1.  Go to your live application URL (e.g., `https://ccsi-app.streamlit.app`).
2.  Paste your free developer access token into the **Gemini API Key** field in the left sidebar configuration panel.
3.  Drag and drop your workshop or pitch-day video asset into the file uploader.
4.  Click the blue **🚀 Process Video & Generate Content Calendar** button.
5.  Review your mobile clips directly in the browser grid, and click **📥 Download Calendar CSV** to save your pre-formatted timeline for immediate import into schedulers like Buffer or Hootsuite.

---

## 🔍 Common Troubleshooting Procedures

### 🚨 Issue 1: Red screen error showing `ModuleNotFoundError: No module named 'moviepy'`
* **Why it happens:** This happens occasionally on free cloud hosting when Streamlit compiles the website container before GitHub finishes syncing the full `requirements.txt` list.
* **How to fix it:** Click **Manage app** in the bottom right corner of your screen. Click the three vertical dots (`⋮`) at the top of the management panel that slides out on the right, and select **Reboot app**. The environment will wipe its cache, cleanly install your editing tools, and launch properly.

### 🚨 Issue 2: App unexpectedly freezes or terminates during processing
* **Why it happens:** Streamlit Community Cloud limits free tier apps to **1 GB of RAM**. Large multi-hour raw files can overload the cloud server's processing memory.
* **How to fix it:** For presentations and rapid evaluations, always utilize a short sample video clip (30 to 60 seconds long). For real production scenarios, split long events into smaller 5-10 minute chapter segments before dropping them into the pipeline.

### 🚨 Issue 3: Interface loads but video slicing fails or shows API errors
* **Why it happens:** The Google AI network can't authenticate your access, usually due to a blank or misspelled API key.
* **How to fix it:** Ensure your free token code is copied exactly from Google AI Studio without extra spaces or symbols.
