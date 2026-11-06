import json
import os
import random
import pandas as pd
import plotly.express as px
import streamlit as st
from google import genai
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="Micro-Content & Social Media Repurposer",
    page_icon="⚡",
    layout="wide"
)

# Initialize Session State
if "repurposed_outputs" not in st.session_state:
    st.session_state.repurposed_outputs = None

# Sidebar Setup & API Configuration
st.sidebar.title("⚙️ AI Engine Settings")
ai_provider = st.sidebar.selectbox(
    "Choose AI Provider", ["Groq (Llama 3)", "Gemini (Google)"], key="ai_provider_select"
)

if ai_provider == "Groq (Llama 3)":
    api_key = st.sidebar.text_input(
        "Groq API Key",
        type="password",
        help="Enter your Groq API key (e.g., gsk_...)",
        key="sidebar_groq_api_key"
    )
else:
    api_key = st.sidebar.text_input(
        "Gemini API Key",
        type="password",
        help="Enter your Google Gemini API key",
        key="sidebar_gemini_api_key"
    )

target_tone = st.sidebar.select_slider(
    "Default Brand Tone",
    options=["Casual & Fast-Paced", "Engaging & Value-First", "Authoritative & B2B"],
    value="Engaging & Value-First"
)

def generate_ai_content(prompt):
    if ai_provider == "Groq (Llama 3)":
        key = api_key or os.environ.get("GROQ_API_KEY")
        if not key:
            return None
        client = Groq(api_key=key)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return completion.choices[0].message.content
    else:
        key = api_key or os.environ.get("GEMINI_API_KEY")
        if not key:
            return None
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return response.text

def fallback_repurpose(source_text):
    first_lines = source_text.strip().split("\n")[0] if source_text else "Key Insight"
    return {
        "linkedin_post": f"🚀 {first_lines}\n\nHere is a key takeaway from our latest deep-dive asset. Continuous iteration and high-value adaptation build massive audience trust.\n\n1. Consistency is key\n2. Adapt native formats\n3. Measure engagement\n\nWhat is your primary content repurposing strategy?\n\n#MarketingOps #ContentStrategy #AI Automation",
        "twitter_thread": [
            f"1/ {first_lines} 🧵",
            "2/ Repurposing long-form content isn't just about cutting snippets—it's about re-engineering core value for platform-native audiences.",
            "3/ LinkedIn demands high structure & spacing. X demands punchy hooks. TikTok requires immediate visual interest.",
            "4/ Automated prompt chains slash output time by 80% while retaining authentic brand tone.",
            "5/ Bookmark this thread and scale your media pipeline today! 🔁"
        ],
        "video_script": {
            "hook_0_3s": f"[Visual: Fast text overlay on screen] '{first_lines[:35]}...'",
            "body_3_30s": "If you're still spending 5 hours turning 1 video into 10 social posts, you're doing it wrong. Here is how top agencies automate content repurposing in seconds...",
            "cta_30_45s": "Save this reel and comment 'AUTOMATE' for our full AI workflow breakdown!"
        },
        "newsletter_snippet": f"**Subject:** Quick Breakdown: {first_lines[:40]}

Hey Team,

Here is a concise summary of our latest analysis. Make sure your content stack is optimized for maximum cross-platform reach without doubling your workload.

Catch you in the next edition!"
    }

def process_repurposing(source_text, tone):
    prompt = f"""
    You are an expert social media content strategist and copywriter.
    Repurpose the following long-form source text into platform-native micro-content formatted in strict JSON:
    
    Source Text:
    {source_text}

    Desired Tone: {tone}

    Return ONLY a valid JSON object with the following exact keys:
    {{
      "linkedin_post": "full formatted LinkedIn post with hook, spacing, bullets, and hashtags",
      "twitter_thread": ["tweet 1 (hook)", "tweet 2", "tweet 3", "tweet 4", "tweet 5 (outro)"],
      "video_script": {{
          "hook_0_3s": "visual and verbal hook",
          "body_3_30s": "core narrative and value points",
          "cta_30_45s": "call to action and visual outro"
      }},
      "newsletter_snippet": "formatted email newsletter section with subject line and summary"
    }}
    """
    raw_res = generate_ai_content(prompt)
    if not raw_res:
        st.info("No API key detected. Rendering template repurposing engine.")
        return fallback_repurpose(source_text)
    try:
        cleaned = raw_res.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)
    except Exception as e:
        st.warning(f"AI response parsing notice: {e}. Loading structured fallback.")
        return fallback_repurpose(source_text)

# Header Section
st.title("⚡ Micro-Content & Social Media Repurposer")
st.markdown("Transform long-form articles, transcripts, and notes into multi-platform social assets instantly.")

# Main Input Section
with st.expander("📥 Source Content Input", expanded=True):
    source_input = st.text_area(
        "Paste Long-Form Article, Transcript, or Blog Post",
        height=200,
        placeholder="Paste your YouTube transcript, blog post, or article text here...",
        key="source_text_input"
    )
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        run_btn = st.button("🚀 Repurpose Assets", use_container_width=True, key="run_repurpose_btn")
    with col_btn2:
        if st.button("📥 Load Sample Marketing Article", key="load_sample_btn"):
            st.session_state.source_text_input = "Content creators and digital marketing agencies waste over 15 hours every week manually adapting a single 20-minute video or 2,000-word blog post across LinkedIn, X/Twitter, and short-form video channels. By building automated LLM prompts into agency workflows, teams can instantly convert a single pillar asset into native LinkedIn articles, viral X threads, and short video scripts with visual cue notes."
            st.rerun()

if run_btn and source_input:
    with st.spinner("Re-engineering content for platform-native algorithms..."):
        st.session_state.repurposed_outputs = process_repurposing(source_input, target_tone)
        st.success("Assets generated successfully!")

# Output Workspace
if st.session_state.repurposed_outputs:
    st.divider()
    res = st.session_state.repurposed_outputs
    
    t1, t2, t3, t4 = st.tabs(["💼 LinkedIn Post", "🧵 X / Twitter Thread", "🎬 Short Video Script", "📧 Newsletter Snippet"])
    
    with t1:
        st.subheader("LinkedIn Native Preview")
        st.text_area("Formatted Copy", value=res.get("linkedin_post", ""), height=250, key="ln_copy_area")
        st.download_button("📥 Copy / Download LinkedIn Post", data=res.get("linkedin_post", ""), file_name="linkedin_post.txt", key="dl_ln")

    with t2:
        st.subheader("X (Twitter) Thread Preview")
        thread_list = res.get("twitter_thread", [])
        if isinstance(thread_list, list):
            for i, tweet in enumerate(thread_list):
                st.text_area(f"Tweet {i+1}", value=tweet, height=80, key=f"tweet_{i}")
            thread_text = "\n\n".join(thread_list)
        else:
            st.text_area("Thread Copy", value=str(thread_list), height=200, key="tweet_alt")
            thread_text = str(thread_list)
        st.download_button("📥 Download X Thread (.txt)", data=thread_text, file_name="twitter_thread.txt", key="dl_tw")

    with t3:
        st.subheader("Short-Form Video Script (Reels / TikTok / Shorts)")
        script_obj = res.get("video_script", {})
        if isinstance(script_obj, dict):
            st.markdown(f"**[0-3s] Hook:** {script_obj.get('hook_0_3s', '')}")
            st.markdown(f"**[3-30s] Core Body:** {script_obj.get('body_3_30s', '')}")
            st.markdown(f"**[30-45s] Call To Action:** {script_obj.get('cta_30_45s', '')}")
            full_script = f"HOOK (0-3s):
{script_obj.get('hook_0_3s','')}

BODY (3-30s):
{script_obj.get('body_3_30s','')}

CTA (30-45s):
{script_obj.get('cta_30_45s','')}"
        else:
            st.write(script_obj)
            full_script = str(script_obj)
        st.download_button("📥 Download Video Script (.txt)", data=full_script, file_name="video_script.txt", key="dl_script")

    with t4:
        st.subheader("Newsletter Snippet Preview")
        st.text_area("Email Content", value=res.get("newsletter_snippet", ""), height=200, key="nl_copy_area")
        st.download_button("📥 Download Newsletter Snippet (.txt)", data=res.get("newsletter_snippet", ""), file_name="newsletter_snippet.txt", key="dl_nl")
