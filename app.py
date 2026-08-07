# ===================== STEP 1: LOAD MODULES =====================

import os
import io
import csv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from typing import List


# ===================== STEP 2: PAGE CONFIG =====================

st.set_page_config(
    page_title="AI YouTube Content Planner",
    page_icon="📺",
    layout="wide"
)


# ===================== STEP 3: NEO BRUTALISM CSS =====================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');

/* Base */
.stApp {
    background-color: #FFFDF5;
    font-family: 'Space Grotesk', sans-serif;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 900 !important;
    color: #000000 !important;
}

/* Title */
.stTitle {
    font-size: 2.5rem !important;
    font-weight: 900 !important;
    color: #000000 !important;
    border-bottom: 4px solid #000000;
    padding-bottom: 8px;
}

/* Subheaders */
.stSubheader {
    font-weight: 700 !important;
    color: #000000 !important;
}

/* Buttons */
.stButton > button {
    background-color: #FF6B6B;
    color: #000000;
    border: 4px solid #000000;
    border-radius: 0px;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    padding: 12px 24px;
    box-shadow: 4px 4px 0px #000000;
    transition: none;
    width: 100%;
}

.stButton > button:hover {
    background-color: #FF6B6B;
    color: #000000;
    box-shadow: 4px 4px 0px #000000;
    transform: none;
}

.stButton > button:active {
    box-shadow: 0px 0px 0px #000000;
    transform: translate(4px, 4px);
}

/* Input fields */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    border: 4px solid #000000 !important;
    border-radius: 0px !important;
    background-color: #FFFFFF !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0px;
    border-bottom: 4px solid #000000;
}

.stTabs [data-baseweb="tab"] {
    border: 4px solid #000000;
    border-bottom: none;
    border-radius: 0px;
    background-color: #FFFFFF;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    padding: 10px 20px;
    margin-right: -4px;
}

.stTabs [aria-selected="true"] {
    background-color: #FFD93D !important;
    color: #000000 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #C4B5FD;
    border-right: 4px solid #000000;
}

section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #000000 !important;
}

/* Alerts */
.stAlert {
    border: 4px solid #000000 !important;
    border-radius: 0px !important;
    box-shadow: 4px 4px 0px #000000 !important;
}

/* Download button */
.stDownloadButton > button {
    background-color: #FFD93D;
    color: #000000;
    border: 4px solid #000000;
    border-radius: 0px;
    box-shadow: 4px 4px 0px #000000;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
}

.stDownloadButton > button:active {
    box-shadow: 0px 0px 0px #000000;
    transform: translate(4px, 4px);
}

/* Markdown content blocks */
.stMarkdown {
    background-color: #FFFFFF;
    border: 4px solid #000000;
    border-radius: 0px;
    padding: 16px;
    box-shadow: 4px 4px 0px #000000;
    margin-bottom: 12px;
}

/* Radio */
.stRadio > div {
    gap: 8px;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: #C4B5FD !important;
    border: 4px solid #000000 !important;
    border-radius: 0px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)


# ===================== STEP 4: PYDANTIC MODELS =====================

class VideoIdea(BaseModel):
    number: int = Field(description="Idea number 1-10")
    title: str = Field(description="Video title")
    hook: str = Field(description="One sentence hook for this idea")

class ThumbnailSuggestion(BaseModel):
    text_overlay: str = Field(description="Text to put on thumbnail")
    visual_description: str = Field(description="Image/visual description")
    color_scheme: str = Field(description="Color suggestion for thumbnail")

class ScriptSection(BaseModel):
    act: str = Field(description="Act name: Hook, Main Content, or CTA")
    timestamp: str = Field(description="Estimated timestamp like 0:00-0:30")
    description: str = Field(description="What happens in this section")
    visual_cue: str = Field(description="B-roll or visual suggestion")

class ContentPlan(BaseModel):
    video_ideas: List[VideoIdea] = Field(description="List of 10 video ideas")
    seo_titles: List[str] = Field(description="5 SEO-friendly titles")
    hashtags: List[str] = Field(description="10 relevant hashtags")
    thumbnail: ThumbnailSuggestion = Field(description="Thumbnail suggestion")
    script_outline: List[ScriptSection] = Field(description="3-act script outline")
    upload_schedule: str = Field(description="Best days and times to upload")
    description: str = Field(description="One video description")


# ===================== STEP 5: SESSION STATE =====================

if "ideas_list" not in st.session_state:
    st.session_state.ideas_list = None
if "full_plan" not in st.session_state:
    st.session_state.full_plan = None


# ===================== STEP 6: API KEY =====================

st.sidebar.title("⚙️ API CONFIG")

GOOGLE_API_KEY = st.sidebar.text_input(
    "GOOGLE API KEY",
    type="password",
    key="api_key_input"
)

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

if GOOGLE_API_KEY:
    st.sidebar.success("✅ API Key Loaded!")
else:
    st.sidebar.info("👈 Enter your Google API Key")


# ===================== STEP 7: MAIN UI =====================

st.title("📺 AI YouTube Content Planner")
st.write("Generate video ideas, SEO titles, thumbnails, scripts and schedules using AI.")

st.subheader("📝 Enter Content Details")

col1, col2 = st.columns(2)

with col1:
    topic = st.text_input(
        "YouTube Topic",
        placeholder="Example: Artificial Intelligence"
    )

    niche = st.selectbox(
        "Your Niche",
        ["Education", "Technology", "Motivation", "Gaming", "Fitness",
         "Finance", "Entertainment", "Travel", "Food", "Other"]
    )

with col2:
    target_audience = st.selectbox(
        "Target Audience",
        ["Global", "India", "USA", "UK", "Students",
         "Working Professionals", "General Audience"]
    )

    tone = st.selectbox(
        "Narrative Tone",
        ["High Energy", "Tech Explainer", "Emotional & Storytelling",
         "Analytical", "Wholesome"]
    )

    video_format = st.radio(
        "Video Format",
        ["Long-form (10m+)", "Shorts/Reels (<60s)"],
        horizontal=True
    )


# ===================== STEP 8: CHAINS =====================

if GOOGLE_API_KEY:

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY
    )

    # --- Chain 1: Brainstorm 10 Ideas ---
    brainstorm_prompt = ChatPromptTemplate.from_template("""
You are a YouTube Content Planning Assistant.

Based on the user's topic, generate exactly 10 video ideas.

Topic: {topic}
Niche: {niche}
Target Audience: {target_audience}
Tone: {tone}
Format: {video_format}

For each idea, provide:
- A number (1-10)
- A catchy video title
- A one sentence hook that makes viewers want to click

Return ONLY a numbered list like:
1. Title — Hook
2. Title — Hook
... up to 10
""")

    brainstorm_chain = brainstorm_prompt | llm | StrOutputParser()

    # --- Chain 2: Full Plan for Selected Idea ---
    full_plan_prompt = ChatPromptTemplate.from_template("""
You are a YouTube Content Planning Assistant.

The user picked this video idea from a list of 10:
**{selected_idea}**

Now generate a COMPLETE content plan for this specific idea.

Topic: {topic}
Niche: {niche}
Target Audience: {target_audience}
Tone: {tone}
Format: {video_format}

Generate in this EXACT format:

SEO TITLES (generate 5):
1. [title]
2. [title]
3. [title]
4. [title]
5. [title]

HASHTAGS (generate 10):
#tag1 #tag2 #tag3 ... list all 10

DESCRIPTION:
Write one engaging YouTube video description (2-3 sentences).

THUMBNAIL:
- Text Overlay: [text to show on thumbnail]
- Visual: [image description]
- Colors: [color scheme]

SCRIPT OUTLINE:
ACT 1 - HOOK (0:00 - 0:30):
Description: [what happens]
Visual Cues: [B-roll suggestion]

ACT 2 - MAIN CONTENT (0:30 - X:XX):
Description: [what happens]
Visual Cues: [B-roll suggestion]

ACT 3 - CTA & OUTRO (X:XX - X:XX):
Description: [what happens]
Visual Cues: [B-roll suggestion]

UPLOAD SCHEDULE:
Best Days: [days]
Best Time: [time]
Reason: [why this schedule]
""")


# ===================== STEP 9: GENERATE IDEAS =====================

    if st.button("🚀 Generate 10 Video Ideas"):

        if topic:
            with st.spinner("🧠 Brainstorming ideas..."):
                try:
                    response = brainstorm_chain.invoke({
                        "topic": topic,
                        "niche": niche,
                        "target_audience": target_audience,
                        "tone": tone,
                        "video_format": video_format
                    })
                    st.session_state.ideas_list = response
                    st.session_state.full_plan = None
                    st.success("✅ Ideas Generated! Pick one below.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Please enter a topic first.")


# ===================== STEP 10: SELECT IDEA =====================

    if st.session_state.ideas_list:

        st.subheader("🎯 Pick a Video Idea")

        with st.expander("📄 View Generated Ideas", expanded=True):
            st.markdown(st.session_state.ideas_list)

        selected_idea = st.text_area(
            "✏️ Copy-paste the idea you want to develop (e.g. '1. AI in Education — How AI is changing classrooms')",
            height=100
        )

        if st.button("📋 Generate Full Plan for This Idea"):

            if selected_idea.strip():
                with st.spinner("📝 Generating full content plan..."):
                    try:
                        response = full_plan_chain.invoke({
                            "selected_idea": selected_idea,
                            "topic": topic,
                            "niche": niche,
                            "target_audience": target_audience,
                            "tone": tone,
                            "video_format": video_format
                        })
                        st.session_state.full_plan = response
                        st.success("✅ Full Plan Generated!")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("⚠️ Please paste the idea you want to develop.")


# ===================== STEP 11: TABBED OUTPUT =====================

    if st.session_state.full_plan:

        st.subheader("📋 Your Content Plan")

        plan_text = st.session_state.full_plan

        # Parse the response into sections
        sections = {
            "titles": "",
            "description": "",
            "thumbnail": "",
            "script": "",
            "schedule": ""
        }

        current = "titles"
        for line in plan_text.split("\n"):
            lower = line.lower().strip()

            if "seo" in lower and "title" in lower:
                current = "titles"
            elif "hashtag" in lower:
                current = "titles"
            elif lower.startswith("description:") or "video description" in lower:
                current = "description"
            elif "thumbnail" in lower:
                current = "thumbnail"
            elif "script" in lower or "act" in lower:
                current = "script"
            elif "schedule" in lower or "upload" in lower:
                current = "schedule"

            sections[current] += line + "\n"

        # Display in tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "💡 Titles & Hashtags",
            "📝 Description",
            "🎨 Thumbnail",
            "🎬 Script Outline",
            "📅 Schedule"
        ])

        with tab1:
            st.markdown(sections["titles"])
        with tab2:
            st.markdown(sections["description"])
        with tab3:
            st.markdown(sections["thumbnail"])
        with tab4:
            st.markdown(sections["script"])
        with tab5:
            st.markdown(sections["schedule"])


# ===================== STEP 12: EXPORT OPTIONS =====================

        st.subheader("⬇️ Export Your Plan")

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="📄 Download as Markdown",
                data=plan_text,
                file_name="youtube_content_plan.md",
                mime="text/markdown"
            )

        with col2:
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer)
            csv_writer.writerow(["Section", "Content"])
            for section_name, content in sections.items():
                csv_writer.writerow([section_name, content.strip()])

            st.download_button(
                label="📊 Download as CSV",
                data=csv_buffer.getvalue(),
                file_name="youtube_content_plan.csv",
                mime="text/csv"
            )

else:

    st.info("👈 Please enter your Google API Key in the sidebar to get started.")
