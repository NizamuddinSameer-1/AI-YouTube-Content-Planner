# ═══════════════════════════════════════════════════════════════════
#  YT CONTENT PLANNER PRO
#  Neo-Brutalism UI · Pydantic Structured Output · Multi-Chain AI
# ═══════════════════════════════════════════════════════════════════

import os
import json
import csv
import io
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="YT Planner Pro",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── NEO-BRUTALISM CSS ────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;700&display=swap');

/* ── Premium Studio Tokens ── */
:root {
  --bk:#0F0F0F;
  --surface:#1A1A2E;
  --panel:#16213E;
  --accent:#E8C547;      /* Warm gold — authoritative, not childish */
  --accent2:#C0392B;     /* Deep crimson — serious red */
  --accent3:#2ECC71;     /* Emerald — for success/positive metrics */
  --muted:#A0AEC0;
  --wh:#F0F4F8;
  --bd-dark:1.5px solid #2D3748;
  --bd-accent:2px solid var(--accent);
  --sh-dark:4px 4px 0 #000000;
  --sh-accent:4px 4px 0 var(--accent);
  --ff-d:'Space Grotesk',sans-serif;
  --ff-m:'IBM Plex Mono',monospace;
}

/* ── Global — dark slate background ── */
.stApp { background:#0F0F1A !important; font-family:var(--ff-d); }
#MainMenu,footer { visibility:hidden; }
.block-container { padding-top:1.5rem !important; max-width:1200px !important; }

/* ── Sidebar — deep navy ── */
[data-testid="stSidebar"] {
  background:linear-gradient(180deg,#0F0F1A 0%,#1A1A2E 100%) !important;
  border-right:1.5px solid #2D3748 !important;
}
[data-testid="stSidebar"] * { font-family:var(--ff-m) !important; color:#CBD5E0 !important; }
[data-testid="stSidebar"] input {
  background:#2D3748 !important; color:var(--wh) !important;
  border:1.5px solid #4A5568 !important; border-radius:4px !important;
}

/* ── Main buttons — gold on dark ── */
.stButton > button {
  background:var(--accent) !important; color:#0F0F0F !important;
  border:2px solid var(--accent) !important; border-radius:3px !important;
  box-shadow:var(--sh-dark) !important; font-family:var(--ff-d) !important;
  font-weight:800 !important; font-size:.85rem !important;
  letter-spacing:.07em !important; text-transform:uppercase !important;
  padding:.6rem 1.6rem !important;
  transition:all .12s ease !important;
}
.stButton > button:hover {
  background:#0F0F0F !important; color:var(--accent) !important;
  border-color:var(--accent) !important;
  box-shadow:0 0 20px rgba(232,197,71,0.25) !important;
  transform:translateY(-1px) !important;
}
.stButton > button:active { transform:translateY(1px) !important; box-shadow:none !important; }

/* ── Download buttons — outlined gold ── */
.stDownloadButton > button {
  background:transparent !important; color:var(--accent) !important;
  border:1.5px solid var(--accent) !important; border-radius:3px !important;
  font-family:var(--ff-d) !important; font-weight:700 !important;
  font-size:.8rem !important; letter-spacing:.06em !important;
  text-transform:uppercase !important;
  transition:all .12s ease !important;
}
.stDownloadButton > button:hover {
  background:var(--accent) !important; color:#0F0F0F !important;
}

/* ── Inputs — dark surface ── */
.stTextInput input, .stTextArea textarea {
  border:1.5px solid #2D3748 !important; border-radius:4px !important;
  background:#1A1A2E !important; font-family:var(--ff-m) !important;
  color:var(--wh) !important;
  transition:border-color .15s ease !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
  border-color:var(--accent) !important;
  box-shadow:0 0 0 3px rgba(232,197,71,0.12) !important;
}
.stSelectbox > div > div {
  border:1.5px solid #2D3748 !important; border-radius:4px !important;
  background:#1A1A2E !important; color:var(--wh) !important;
}

/* ── Tabs — dark with gold active ── */
.stTabs [data-baseweb="tab-list"] {
  gap:3px !important; border-bottom:1.5px solid #2D3748 !important;
  background:transparent !important;
}
.stTabs [data-baseweb="tab"] {
  border:1.5px solid #2D3748 !important; border-bottom:none !important;
  background:#1A1A2E !important; border-radius:4px 4px 0 0 !important;
  font-family:var(--ff-d) !important; font-weight:600 !important;
  padding:.5rem 1.1rem !important; color:#718096 !important;
  transition:all .12s ease !important;
}
.stTabs [aria-selected="true"] {
  background:#16213E !important; color:var(--accent) !important;
  border-color:var(--accent) !important; border-bottom:none !important;
}
.stTabs [data-baseweb="tab-panel"] {
  border:1.5px solid #2D3748 !important; border-top:none !important;
  padding:1.5rem !important; background:#16213E !important;
}

/* ── Alerts & Metrics ── */
.stSuccess { background:#0D2818 !important; border:1.5px solid #2ECC71 !important;
             border-left:4px solid #2ECC71 !important; border-radius:4px !important; }
.stInfo    { background:#0D1A2E !important; border:1.5px solid #3B82F6 !important;
             border-left:4px solid #3B82F6 !important; border-radius:4px !important; }
.stWarning { background:#2D1F00 !important; border:1.5px solid var(--accent) !important;
             border-left:4px solid var(--accent) !important; border-radius:4px !important; }
.stError   { background:#2D0A0A !important; border:1.5px solid var(--accent2) !important;
             border-left:4px solid var(--accent2) !important; border-radius:4px !important; }

[data-testid="stMetric"] {
  background:#1A1A2E !important; border:1.5px solid #2D3748 !important;
  border-radius:6px !important; padding:.8rem 1rem !important;
  border-left:3px solid var(--accent) !important;
}
[data-testid="stMetricValue"] {
  font-family:var(--ff-d) !important; font-weight:800 !important;
  color:var(--accent) !important;
}
[data-testid="stMetricLabel"] { font-family:var(--ff-m) !important; color:#A0AEC0 !important; }

/* ── HR ── */
hr { border:1px solid #2D3748 !important; margin:1.5rem 0 !important; }

/* ── Markdown headings in dark mode ── */
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3 { color:#F0F4F8 !important; }
.stMarkdown p { color:#CBD5E0 !important; }
</style>
""", unsafe_allow_html=True)


# ── HEADER BANNER ────────────────────────────────────────────────────────────

st.markdown("""
<div style="background:linear-gradient(135deg,#1A1A2E 0%,#16213E 60%,#0F3460 100%);
            border:1.5px solid #2D3748;border-left:4px solid #E8C547;
            border-radius:8px;padding:2.5rem 3rem;margin-bottom:2rem;
            position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;right:0;width:300px;height:100%;
              background:linear-gradient(90deg,transparent,rgba(232,197,71,0.04));
              pointer-events:none;"></div>
  <div style="display:flex;align-items:center;gap:.6rem;margin-bottom:1rem;">
    <span style="display:inline-block;width:8px;height:8px;border-radius:50%;
                 background:#E8C547;box-shadow:0 0 8px rgba(232,197,71,0.6);"></span>
    <span style="font-family:'IBM Plex Mono',monospace;font-size:.65rem;font-weight:700;
                 color:#E8C547;letter-spacing:.2em;text-transform:uppercase;">
      STUDIO DASHBOARD &nbsp;·&nbsp; AI-POWERED
    </span>
  </div>
  <div style="font-family:'Space Grotesk',sans-serif;font-size:2.6rem;font-weight:900;
              color:#F0F4F8;line-height:1.05;letter-spacing:-.03em;">
    YT CONTENT<br>
    <span style="color:#E8C547;">PLANNER</span> PRO
  </div>
  <div style="font-family:'IBM Plex Mono',monospace;font-size:.8rem;color:#718096;
              margin:1rem 0 0;letter-spacing:.04em;">
    Ideas &nbsp;→&nbsp; Script &nbsp;→&nbsp; Hooks &nbsp;→&nbsp; Strategy &nbsp;→&nbsp; Export
  </div>
</div>
""", unsafe_allow_html=True)


# ── SESSION STATE INIT ───────────────────────────────────────────────────────

_defaults = {
    "api_key": "", "topic": "", "niche": "Education",
    "target_audience": "Global", "video_format": "Long-form (10m+)",
    "tone": "High Energy", "content_plan": None,
    "script_data": None, "generation_done": False,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── SIDEBAR ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        '<p style="font-family:\'IBM Plex Mono\',monospace;font-size:.7rem;'
        'letter-spacing:.15em;color:#E8C547;margin-bottom:.4rem;">▶ API CONFIG</p>',
        unsafe_allow_html=True,
    )

    # Prefer st.secrets, fallback to text_input for local dev
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✓ Key loaded from st.secrets")
    except Exception:
        api_key = st.text_input("GOOGLE API KEY", type="password", key="api_key_input")
        if api_key:
            st.session_state.api_key = api_key
            st.success("✓ API Key loaded")
        else:
            st.info("Enter your Google API Key")

    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'IBM Plex Mono',monospace;font-size:.7rem;color:#718096;line-height:1.9;">
      <p style="letter-spacing:.12em;color:#E8C547;margin-bottom:.5rem;">▶ WORKFLOW</p>
      <p>① Fill topic &amp; settings</p>
      <p>② Generate content plan</p>
      <p>③ Browse ideas &amp; titles</p>
      <p>④ Pick a winning idea</p>
      <p>⑤ Generate script + hooks</p>
      <p>⑥ Export everything</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'IBM Plex Mono',monospace;font-size:.65rem;color:#4A5568;line-height:1.6;">
      Deploy tip: add GOOGLE_API_KEY to<br>.streamlit/secrets.toml to skip<br>entering it every session.
    </div>
    """, unsafe_allow_html=True)


# ── PYDANTIC SCHEMAS ─────────────────────────────────────────────────────────

class VideoIdea(BaseModel):
    title: str = Field(description="Catchy, specific video title")
    description: str = Field(description="2-sentence hook + value proposition")

class ThumbnailConcept(BaseModel):
    text_overlay: str = Field(description="Bold 3-6 word thumbnail text")
    visual_concept: str = Field(description="Background image / visual idea")
    mood: str = Field(description="Color mood / emotional vibe")

class ContentPlan(BaseModel):
    video_ideas: List[VideoIdea] = Field(description="10 video ideas")
    seo_titles: List[str] = Field(description="5 SEO-optimised YouTube titles")
    description: str = Field(description="150-word YouTube video description")
    hashtags: List[str] = Field(description="10 relevant hashtags with # prefix")
    thumbnail: ThumbnailConcept
    upload_days: List[str] = Field(description="Best 2-3 days to upload")
    upload_time: str = Field(description="Optimal upload time with timezone")

class RetentionHook(BaseModel):
    hook_type: str = Field(description="Visual / Verbal / Text-on-Screen")
    hook_text: str = Field(description="The exact hook content")
    why_it_works: str = Field(description="Psychological reason this hook retains viewers")

class ScriptSection(BaseModel):
    timestamp: str = Field(description="Time range e.g. 0:00 - 0:45")
    section_title: str = Field(description="Name of this section")
    content_notes: str = Field(description="What to say/show in this section")
    broll_cue: str = Field(description="B-roll footage suggestion")
    cta: Optional[str] = Field(default=None, description="Call-to-action text if applicable")

class ScriptOutline(BaseModel):
    video_title: str
    total_duration: str
    hooks: List[RetentionHook] = Field(description="3 hooks: Visual, Verbal, Text-on-Screen")
    sections: List[ScriptSection] = Field(description="5-7 timestamped script sections")
    closing_cta: str


# ── HELPERS ──────────────────────────────────────────────────────────────────

def build_llm(key: str) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=key,
        temperature=0.85,
    )

def clean_json(raw: str) -> dict:
    """Strip markdown fences and parse JSON."""
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())

def badge(label: str, bg: str = "#E8C547", fg: str = "#0F0F0F") -> str:
    return (
        f'<span style="font-family:\'IBM Plex Mono\',monospace;font-size:.66rem;'
        f'font-weight:700;letter-spacing:.14em;background:{bg};color:{fg};'
        f'padding:.18rem .6rem;border-radius:2px;">{label}</span>'
    )

def section_card(step_label: str, step_bg: str, step_fg: str, title: str, subtitle: str = "") -> str:
    sub = (
        f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:.76rem;'
        f'color:#718096;margin-top:.4rem;">{subtitle}</div>'
        if subtitle else ""
    )
    return (
        f'<div style="border:1.5px solid #2D3748;border-left:4px solid {step_bg};'
        f'border-radius:6px;padding:1.5rem 1.8rem;background:#1A1A2E;margin-bottom:1rem;">'
        f'{badge(step_label, step_bg, step_fg)}'
        f'<div style="font-family:\'Space Grotesk\',sans-serif;font-weight:800;'
        f'font-size:1.25rem;margin:.7rem 0 0;color:#F0F4F8;">{title}</div>'
        f'{sub}</div>'
    )


# ── CHAIN 1: Content Plan ─────────────────────────────────────────────────────

_PLAN_PROMPT = ChatPromptTemplate.from_template("""
You are an elite YouTube content strategist. Build a data-driven content plan.

Topic: {topic}
Niche: {niche}
Target Audience: {target_audience}
Video Format: {video_format}
Tone / Style: {tone}

Return ONLY a valid JSON object — no markdown fences, no preamble, no trailing text:
{{
  "video_ideas": [{{"title":"...","description":"..."}}],
  "seo_titles": ["...","...","...","...","..."],
  "description": "...",
  "hashtags": ["#...","#..."],
  "thumbnail": {{"text_overlay":"...","visual_concept":"...","mood":"..."}},
  "upload_days": ["...","..."],
  "upload_time": "..."
}}

Rules: exactly 10 video_ideas · exactly 5 seo_titles · exactly 10 hashtags.
Tailor everything tightly to the format ({video_format}) and tone ({tone}).
""")

def run_plan_chain(key, topic, niche, audience, fmt, tone) -> ContentPlan:
    chain = _PLAN_PROMPT | build_llm(key) | StrOutputParser()
    raw = chain.invoke(dict(topic=topic, niche=niche, target_audience=audience,
                            video_format=fmt, tone=tone))
    return ContentPlan(**clean_json(raw))


# ── CHAIN 2: Script Outline ───────────────────────────────────────────────────

_SCRIPT_PROMPT = ChatPromptTemplate.from_template("""
You are a professional YouTube scriptwriter. Create a production-ready script outline.

Video Title: {title}
Topic: {topic}
Format: {video_format}
Tone: {tone}
Audience: {target_audience}

Return ONLY valid JSON — no fences, no extra text:
{{
  "video_title": "...",
  "total_duration": "...",
  "hooks": [
    {{"hook_type":"Visual","hook_text":"...","why_it_works":"..."}},
    {{"hook_type":"Verbal","hook_text":"...","why_it_works":"..."}},
    {{"hook_type":"Text-on-Screen","hook_text":"...","why_it_works":"..."}}
  ],
  "sections": [
    {{"timestamp":"0:00 - 0:30","section_title":"Hook","content_notes":"...","broll_cue":"...","cta":null}},
    {{"timestamp":"0:30 - 2:00","section_title":"Intro","content_notes":"...","broll_cue":"...","cta":null}}
  ],
  "closing_cta": "..."
}}

Produce 5-7 sections total. Make timestamps realistic for {video_format}.
""")

def run_script_chain(key, title, topic, fmt, tone, audience) -> ScriptOutline:
    chain = _SCRIPT_PROMPT | build_llm(key) | StrOutputParser()
    raw = chain.invoke(dict(title=title, topic=topic, video_format=fmt,
                            tone=tone, target_audience=audience))
    return ScriptOutline(**clean_json(raw))


# ── EXPORT HELPERS ────────────────────────────────────────────────────────────

def plan_to_markdown(plan: ContentPlan, topic: str) -> str:
    lines = [f"# YouTube Content Plan: {topic}\n"]
    lines += ["## 💡 Video Ideas\n"]
    lines += [f"**{i+1}. {x.title}**\n{x.description}\n" for i, x in enumerate(plan.video_ideas)]
    lines += ["\n## 🔍 SEO Titles\n"] + [f"- {t}" for t in plan.seo_titles]
    lines += ["\n## 📝 Description\n", plan.description]
    lines += ["\n## # Hashtags\n", " ".join(plan.hashtags)]
    lines += [
        "\n## 🎨 Thumbnail Concept\n",
        f"**Text:** {plan.thumbnail.text_overlay}",
        f"**Visual:** {plan.thumbnail.visual_concept}",
        f"**Mood:** {plan.thumbnail.mood}",
    ]
    lines += [
        "\n## 📅 Upload Schedule\n",
        f"**Best Days:** {', '.join(plan.upload_days)}",
        f"**Optimal Time:** {plan.upload_time}",
    ]
    return "\n".join(lines)

def plan_to_csv(plan: ContentPlan) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["Type", "Content"])
    [w.writerow(["Video Idea", f"{x.title}: {x.description}"]) for x in plan.video_ideas]
    [w.writerow(["SEO Title", t]) for t in plan.seo_titles]
    w.writerow(["Description", plan.description])
    w.writerow(["Hashtags", " ".join(plan.hashtags)])
    w.writerow(["Thumbnail Text", plan.thumbnail.text_overlay])
    w.writerow(["Upload Days", ", ".join(plan.upload_days)])
    w.writerow(["Upload Time", plan.upload_time])
    return buf.getvalue()

def script_to_markdown(script: ScriptOutline) -> str:
    lines = [f"# Script: {script.video_title}", f"*Duration: {script.total_duration}*\n"]
    lines += ["\n## ⚡ Retention Hooks\n"]
    for h in script.hooks:
        lines += [f"### {h.hook_type} Hook", f'**"{h.hook_text}"**', f"*Why it works:* {h.why_it_works}\n"]
    lines += ["\n## 📋 Script Sections\n"]
    for s in script.sections:
        lines.append(f"### `{s.timestamp}` — {s.section_title}")
        lines.append(s.content_notes)
        lines.append(f"*B-roll:* {s.broll_cue}")
        if s.cta:
            lines.append(f"*CTA:* {s.cta}")
        lines.append("")
    lines += [f"\n## 🎯 Closing CTA\n{script.closing_cta}"]
    return "\n".join(lines)


# ════════════════════════════════════════════════════════════════════
#   MAIN UI
# ════════════════════════════════════════════════════════════════════

# ── STEP 1: INPUT ─────────────────────────────────────────────────────────────

st.markdown(section_card("STEP 01 / INPUT", "#E8C547", "#0F0F0F", "What are we creating today?"),
            unsafe_allow_html=True)

c1, c2 = st.columns([3, 1])
with c1:
    topic_val = st.text_input(
        "🎯 YouTube Topic",
        placeholder="e.g. How to use AI to learn anything 10× faster",
        value=st.session_state.topic,
    )
    if topic_val:
        st.session_state.topic = topic_val

with c2:
    niches = ["Education","Technology","Motivation","Gaming","Fitness",
              "Finance","Entertainment","Travel","Food","Other"]
    niche_val = st.selectbox("📂 Niche", niches,
                             index=niches.index(st.session_state.niche))
    st.session_state.niche = niche_val

c3, c4, c5 = st.columns(3)
with c3:
    aud_opts = ["Global","India","USA","UK","Students","Working Professionals","General Audience"]
    aud_val = st.selectbox("🌍 Target Audience", aud_opts,
                           index=aud_opts.index(st.session_state.target_audience))
    st.session_state.target_audience = aud_val

with c4:
    fmt_opts = ["Long-form (10m+)", "Mid-length (5-10m)", "Shorts / Reels (<60s)"]
    fmt_idx = fmt_opts.index(st.session_state.video_format) if st.session_state.video_format in fmt_opts else 0
    fmt_val = st.selectbox("🎬 Video Format", fmt_opts, index=fmt_idx)
    st.session_state.video_format = fmt_val

with c5:
    tone_opts = ["High Energy","Tech Explainer","Emotional & Storytelling",
                 "Analytical","Wholesome","Comedic","Authoritative"]
    tone_idx = tone_opts.index(st.session_state.tone) if st.session_state.tone in tone_opts else 0
    tone_val = st.selectbox("🎭 Tone", tone_opts, index=tone_idx)
    st.session_state.tone = tone_val

# ── GENERATE BUTTON ───────────────────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)

if not api_key:
    st.info("👈 Enter your Google API Key in the sidebar to unlock the generator.")
else:
    btn_col, _ = st.columns([1, 3])
    with btn_col:
        generate_clicked = st.button("⚡ GENERATE CONTENT PLAN", use_container_width=True)

    if generate_clicked:
        if not st.session_state.topic.strip():
            st.warning("⚠️ Please enter a YouTube topic first.")
        else:
            with st.spinner("🧠 Brainstorming your content plan…"):
                try:
                    plan = run_plan_chain(
                        api_key,
                        st.session_state.topic,
                        st.session_state.niche,
                        st.session_state.target_audience,
                        st.session_state.video_format,
                        st.session_state.tone,
                    )
                    st.session_state.content_plan = plan
                    st.session_state.generation_done = True
                    st.session_state.script_data = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Generation failed: {e}")


# ════════════════════════════════════════════════════════════════════
#   STEP 2 — CONTENT PLAN RESULTS
# ════════════════════════════════════════════════════════════════════

if st.session_state.content_plan:
    plan: ContentPlan = st.session_state.content_plan

    st.markdown("---")
    st.markdown(section_card(
        "STEP 02 / CONTENT PLAN", "#C0392B", "#FFFFFF",
        "Your Personalised Content Plan",
    ), unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "💡 Ideas & Titles",
        "🎨 Visuals & SEO",
        "📅 Strategy",
        "📦 Export",
    ])

    # ── TAB 1: IDEAS & TITLES ─────────────────────────────────────────────────
    with tab1:
        st.markdown("### 🧠 10 Video Ideas")

        # Premium dark cards with rotating left-border accents
        CARD_ACCENT = ["#E8C547","#C0392B","#2ECC71","#3B82F6","#A855F7",
                       "#E8C547","#C0392B","#2ECC71","#3B82F6","#A855F7"]

        col_a, col_b = st.columns(2)
        for i, idea in enumerate(plan.video_ideas):
            with (col_a if i % 2 == 0 else col_b):
                acc = CARD_ACCENT[i]
                st.markdown(f"""
                <div style="border:1.5px solid #2D3748;border-left:4px solid {acc};
                            border-radius:6px;padding:1rem 1.2rem;margin-bottom:.8rem;
                            background:#1A1A2E;">
                  <span style="font-family:'IBM Plex Mono',monospace;font-size:.6rem;
                               font-weight:700;color:{acc};letter-spacing:.1em;">IDEA #{i+1:02d}</span>
                  <p style="font-family:'Space Grotesk',sans-serif;font-weight:700;
                            font-size:.95rem;margin:.35rem 0 .4rem;color:#F0F4F8;">{idea.title}</p>
                  <p style="font-family:'IBM Plex Mono',monospace;font-size:.75rem;
                            color:#718096;margin:0;line-height:1.6;">{idea.description}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🔍 SEO-Friendly Titles")
        for t in plan.seo_titles:
            st.markdown(f"""
            <div style="border:1.5px solid #2D3748;border-left:3px solid #E8C547;
                        padding:.7rem 1rem;margin-bottom:.4rem;border-radius:4px;
                        background:#16213E;font-family:'Space Grotesk',sans-serif;
                        font-weight:600;font-size:.92rem;color:#F0F4F8;">
              🎯 {t}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📝 Ready-to-Use Description")
        st.markdown(f"""
        <div style="border:1.5px solid #2D3748;padding:1.2rem 1.4rem;background:#16213E;
                    border-radius:6px;font-family:'IBM Plex Mono',monospace;
                    font-size:.82rem;line-height:1.9;color:#A0AEC0;">
          {plan.description}
        </div>
        """, unsafe_allow_html=True)

    # ── TAB 2: VISUALS & SEO ──────────────────────────────────────────────────
    with tab2:
        c_th, c_ht = st.columns([1, 1])

        with c_th:
            st.markdown("### 🎨 Thumbnail Mockup Preview")
            st.markdown(f"""
            <div style="border:1.5px solid #2D3748;border-radius:8px;overflow:hidden;">
              <div style="background:linear-gradient(135deg,#C0392B 0%,#8B0000 100%);
                          padding:2.5rem 1.5rem;text-align:center;
                          border-bottom:1.5px solid #2D3748;min-height:130px;
                          display:flex;align-items:center;justify-content:center;">
                <span style="font-family:'Space Grotesk',sans-serif;font-size:1.65rem;
                             font-weight:900;color:#F0F4F8;text-transform:uppercase;
                             line-height:1.1;letter-spacing:-.02em;
                             text-shadow:0 2px 12px rgba(0,0,0,0.5);">{plan.thumbnail.text_overlay}</span>
              </div>
              <div style="background:#1A1A2E;padding:1rem 1.2rem;">
                <div style="margin-bottom:.6rem;">
                  <span style="font-family:'IBM Plex Mono',monospace;font-size:.6rem;
                               color:#4A5568;display:block;margin-bottom:.2rem;letter-spacing:.1em;">VISUAL CONCEPT</span>
                  <span style="font-family:'Space Grotesk',sans-serif;font-size:.88rem;
                               font-weight:600;color:#F0F4F8;">{plan.thumbnail.visual_concept}</span>
                </div>
                <div>
                  <span style="font-family:'IBM Plex Mono',monospace;font-size:.6rem;
                               color:#4A5568;display:block;margin-bottom:.2rem;letter-spacing:.1em;">MOOD &amp; PALETTE</span>
                  <span style="font-family:'Space Grotesk',sans-serif;font-size:.88rem;
                               font-weight:600;color:#F0F4F8;">{plan.thumbnail.mood}</span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        with c_ht:
            st.markdown("### # Hashtag Cloud")
            TAG_COLORS = ["#E8C547","#C0392B","#2ECC71","#3B82F6","#A855F7"] * 2
            TAG_FG     = ["#0F0F0F","#FFFFFF","#0F0F0F","#FFFFFF","#FFFFFF"] * 2
            tags_html = "".join([
                f'<span style="display:inline-block;background:{TAG_COLORS[i%10]};'
                f'color:{TAG_FG[i%10]};'
                f'font-family:\'IBM Plex Mono\',monospace;font-size:.72rem;font-weight:700;'
                f'padding:.3rem .7rem;margin:.25rem;border-radius:3px;'
                f'letter-spacing:.05em;">{tag}</span>'
                for i, tag in enumerate(plan.hashtags)
            ])
            st.markdown(f"""
            <div style="border:1.5px solid #2D3748;padding:1rem;background:#16213E;
                        border-radius:6px;line-height:2.5;">
              {tags_html}
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 3: STRATEGY ───────────────────────────────────────────────────────
    with tab3:
        c_s1, c_s2 = st.columns(2)

        with c_s1:
            st.markdown("### 📅 Upload Schedule")
            days_display = " &nbsp;·&nbsp; ".join(plan.upload_days)
            st.markdown(f"""
            <div style="border:1.5px solid #2D3748;border-left:4px solid #E8C547;
                        padding:1.4rem;border-radius:6px;background:#1A1A2E;margin-bottom:1rem;">
              <span style="font-family:'IBM Plex Mono',monospace;font-size:.6rem;color:#4A5568;
                           display:block;margin-bottom:.4rem;letter-spacing:.12em;">BEST DAYS TO UPLOAD</span>
              <span style="font-family:'Space Grotesk',sans-serif;font-size:1.2rem;
                           font-weight:800;color:#E8C547;">{days_display}</span>
            </div>
            <div style="border:1.5px solid #2D3748;border-left:4px solid #2ECC71;
                        padding:1.4rem;border-radius:6px;background:#1A1A2E;">
              <span style="font-family:'IBM Plex Mono',monospace;font-size:.6rem;color:#4A5568;
                           display:block;margin-bottom:.4rem;letter-spacing:.12em;">OPTIMAL UPLOAD TIME</span>
              <span style="font-family:'Space Grotesk',sans-serif;font-size:1.2rem;
                           font-weight:800;color:#2ECC71;">{plan.upload_time}</span>
            </div>
            """, unsafe_allow_html=True)

        with c_s2:
            st.markdown("### 📊 Plan Metrics")
            st.metric("Video Format", st.session_state.video_format)
            st.metric("Tone", st.session_state.tone)
            st.metric("Target Audience", st.session_state.target_audience)
            st.metric("Ideas Generated", f"{len(plan.video_ideas)}/10")

    # ── TAB 4: EXPORT ─────────────────────────────────────────────────────────
    with tab4:
        st.markdown("### 📦 Export Your Content Plan")

        md_data  = plan_to_markdown(plan, st.session_state.topic)
        csv_data = plan_to_csv(plan)
        slug = st.session_state.topic[:20].replace(" ", "_").lower()

        e1, e2, e3 = st.columns(3)
        with e1:
            st.download_button(
                "⬇️ MARKDOWN",
                data=md_data,
                file_name=f"yt_plan_{slug}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with e2:
            st.download_button(
                "⬇️ CSV / NOTION",
                data=csv_data,
                file_name=f"yt_plan_{slug}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with e3:
            st.download_button(
                "⬇️ PLAIN TEXT",
                data=md_data,
                file_name=f"yt_plan_{slug}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 Import the CSV directly into Notion, Airtable, or Google Sheets to use it as a content calendar.")


# ════════════════════════════════════════════════════════════════════
#   STEP 3 — IDEA SELECTOR + SCRIPT + HOOKS
# ════════════════════════════════════════════════════════════════════

if st.session_state.content_plan:
    plan: ContentPlan = st.session_state.content_plan

    st.markdown("---")
    st.markdown(section_card(
        "STEP 03 / DEEP-DIVE", "#2ECC71", "#0F0F0F",
        "Pick a Winning Idea → Build the Full Script",
        "Select one idea and let AI generate a timestamped script outline + 3-second retention hooks.",
    ), unsafe_allow_html=True)

    idea_labels = [f"{i+1}. {x.title}" for i, x in enumerate(plan.video_ideas)]
    chosen_label = st.selectbox("🎯 Choose the idea to develop:", idea_labels, key="idea_selector")

    s_col, _ = st.columns([1, 3])
    with s_col:
        if st.button("📜 GENERATE SCRIPT + HOOKS", use_container_width=True):
            idx = idea_labels.index(chosen_label)
            chosen_title = plan.video_ideas[idx].title
            with st.spinner("✍️ Writing your script outline…"):
                try:
                    script = run_script_chain(
                        api_key,
                        chosen_title,
                        st.session_state.topic,
                        st.session_state.video_format,
                        st.session_state.tone,
                        st.session_state.target_audience,
                    )
                    st.session_state.script_data = script
                    st.rerun()
                except Exception as e:
                    st.error(f"Script generation failed: {e}")

    # ── SCRIPT OUTPUT ─────────────────────────────────────────────────────────

    if st.session_state.script_data:
        script: ScriptOutline = st.session_state.script_data

        st.markdown(f"""
        <div style="border:1.5px solid #2D3748;border-left:4px solid #E8C547;
                    padding:1.5rem 1.8rem;margin:1rem 0;border-radius:6px;background:#1A1A2E;">
          {badge("SCRIPT OUTLINE", "#E8C547", "#0F0F0F")}
          <div style="font-family:'Space Grotesk',sans-serif;font-weight:800;font-size:1.25rem;
                      margin:.6rem 0 .2rem;color:#F0F4F8;">{script.video_title}</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:.73rem;
                      color:#4A5568;">⏱ {script.total_duration}</div>
        </div>
        """, unsafe_allow_html=True)

        stab1, stab2 = st.tabs(["⚡ 3-Second Hooks", "📋 Full Script"])

        # ── HOOKS TAB ────────────────────────────────────────────────────────
        with stab1:
            st.markdown("### ⚡ First-3-Second Retention Hooks")
            st.markdown(
                '<p style="font-family:\'IBM Plex Mono\',monospace;font-size:.75rem;'
                'opacity:.6;margin-bottom:1.2rem;">These opening hooks stop the scroll. '
                'Use one, or A/B test all three.</p>',
                unsafe_allow_html=True,
            )

            HOOK_ACCENT = {"Visual": "#E8C547", "Verbal": "#3B82F6", "Text-on-Screen": "#C0392B"}

            for hook in script.hooks:
                acc = HOOK_ACCENT.get(hook.hook_type, "#E8C547")
                st.markdown(f"""
                <div style="border:1.5px solid #2D3748;border-left:4px solid {acc};
                            border-radius:6px;margin-bottom:1rem;overflow:hidden;background:#1A1A2E;">
                  <div style="padding:.6rem 1.2rem;border-bottom:1px solid #2D3748;
                              display:flex;align-items:center;gap:.6rem;">
                    <span style="display:inline-block;width:8px;height:8px;border-radius:50%;
                                 background:{acc};flex-shrink:0;"></span>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:.66rem;
                                 font-weight:700;color:{acc};letter-spacing:.14em;">
                      {hook.hook_type.upper()} HOOK
                    </span>
                  </div>
                  <div style="padding:1rem 1.2rem;background:#16213E;">
                    <p style="font-family:'Space Grotesk',sans-serif;font-weight:700;
                              font-size:1rem;margin:0 0 .5rem;color:#F0F4F8;line-height:1.5;">
                      "{hook.hook_text}"
                    </p>
                    <p style="font-family:'IBM Plex Mono',monospace;font-size:.75rem;
                              color:#718096;margin:0;line-height:1.6;">
                      💡 {hook.why_it_works}
                    </p>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        # ── FULL SCRIPT TAB ───────────────────────────────────────────────────
        with stab2:
            st.markdown("### 📋 Timestamped Script Sections")

            for sec in script.sections:
                cta_block = (
                    f'<div style="margin-top:.6rem;background:rgba(232,197,71,0.12);'
                    f'padding:.3rem .7rem;display:inline-block;border-radius:3px;'
                    f'border:1px solid rgba(232,197,71,0.4);'
                    f'font-family:\'IBM Plex Mono\',monospace;font-size:.68rem;'
                    f'font-weight:700;color:#E8C547;">'
                    f'📣 CTA: {sec.cta}</div>'
                ) if sec.cta else ""

                st.markdown(f"""
                <div style="border:1.5px solid #2D3748;margin-bottom:.7rem;
                            border-radius:6px;overflow:hidden;">
                  <div style="background:#0F3460;padding:.5rem 1rem;
                              display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-family:'Space Grotesk',sans-serif;font-weight:700;
                                 color:#F0F4F8;font-size:.9rem;">{sec.section_title}</span>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:.66rem;
                                 color:#E8C547;background:rgba(232,197,71,0.12);
                                 padding:.15rem .5rem;border-radius:2px;">{sec.timestamp}</span>
                  </div>
                  <div style="padding:.9rem 1rem;background:#1A1A2E;">
                    <p style="font-family:'IBM Plex Mono',monospace;font-size:.8rem;
                              color:#CBD5E0;margin:0 0 .4rem;line-height:1.7;">{sec.content_notes}</p>
                    <p style="font-family:'IBM Plex Mono',monospace;font-size:.7rem;
                              color:#4A5568;margin:0;">🎬 {sec.broll_cue}</p>
                    {cta_block}
                  </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="border:1.5px solid #C0392B;border-left:4px solid #C0392B;
                        padding:1.1rem 1.4rem;background:#2D0A0A;
                        border-radius:6px;margin-top:1rem;">
              <span style="font-family:'IBM Plex Mono',monospace;font-size:.6rem;
                           color:#C0392B;display:block;margin-bottom:.4rem;
                           letter-spacing:.14em;">📣 CLOSING CTA</span>
              <span style="font-family:'Space Grotesk',sans-serif;font-weight:700;
                           font-size:1rem;color:#F0F4F8;">{script.closing_cta}</span>
            </div>
            """, unsafe_allow_html=True)

        # Script export button
        st.markdown("<br>", unsafe_allow_html=True)
        sc_md = script_to_markdown(script)
        st.download_button(
            "⬇️ DOWNLOAD SCRIPT (MARKDOWN)",
            data=sc_md,
            file_name=f"script_{script.video_title[:20].replace(' ','_')}.md",
            mime="text/markdown",
        )


# ── FOOTER ───────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style="text-align:center;font-family:'IBM Plex Mono',monospace;font-size:.68rem;
            padding:.8rem 0;color:#2D3748;letter-spacing:.1em;">
  YT CONTENT PLANNER PRO &nbsp;·&nbsp; STREAMLIT + LANGCHAIN + GEMINI 2.5 FLASH
</div>
""", unsafe_allow_html=True)
