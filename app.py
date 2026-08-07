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

/* ── Tokens ── */
:root {
  --bk:#0D0D0D; --wh:#FAFAF0; --yw:#FFE500;
  --rd:#FF3B00; --bl:#00C4FF; --gn:#00E676;
  --bd:2.5px solid #0D0D0D;
  --sh:4px 4px 0 #0D0D0D; --sh-lg:6px 6px 0 #0D0D0D;
  --ff-d:'Space Grotesk',sans-serif;
  --ff-m:'IBM Plex Mono',monospace;
}

/* ── Global ── */
.stApp { background:var(--wh) !important; font-family:var(--ff-d); }
#MainMenu,footer { visibility:hidden; }
.block-container { padding-top:1.5rem !important; max-width:1200px !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background:var(--bk) !important; border-right:var(--bd) !important; }
[data-testid="stSidebar"] * { font-family:var(--ff-m) !important; color:var(--wh) !important; }
[data-testid="stSidebar"] input {
  background:var(--yw) !important; color:var(--bk) !important;
  border:var(--bd) !important; border-radius:0 !important;
}

/* ── Buttons ── */
.stButton > button {
  background:var(--yw) !important; color:var(--bk) !important;
  border:var(--bd) !important; border-radius:0 !important;
  box-shadow:var(--sh) !important; font-family:var(--ff-d) !important;
  font-weight:800 !important; font-size:.85rem !important;
  letter-spacing:.06em !important; text-transform:uppercase !important;
  padding:.6rem 1.4rem !important;
  transition:transform .08s ease, box-shadow .08s ease, background .1s ease !important;
}
.stButton > button:hover {
  transform:translate(-2px,-2px) !important; box-shadow:var(--sh-lg) !important;
  background:var(--rd) !important; color:var(--wh) !important;
}
.stButton > button:active { transform:translate(2px,2px) !important; box-shadow:none !important; }

/* ── Download buttons ── */
.stDownloadButton > button {
  background:var(--bl) !important; color:var(--bk) !important;
  border:var(--bd) !important; border-radius:0 !important;
  box-shadow:var(--sh) !important; font-family:var(--ff-d) !important;
  font-weight:800 !important; font-size:.8rem !important;
  letter-spacing:.06em !important; text-transform:uppercase !important;
  transition:transform .08s ease, box-shadow .08s ease !important;
}
.stDownloadButton > button:hover {
  transform:translate(-2px,-2px) !important; box-shadow:var(--sh-lg) !important;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
  border:var(--bd) !important; border-radius:0 !important;
  background:#fff !important; font-family:var(--ff-m) !important;
  color:var(--bk) !important; box-shadow:var(--sh) !important;
}
.stSelectbox > div > div {
  border:var(--bd) !important; border-radius:0 !important;
  box-shadow:var(--sh) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  gap:4px !important; border-bottom:2.5px solid var(--bk) !important;
  background:transparent !important;
}
.stTabs [data-baseweb="tab"] {
  border:var(--bd) !important; border-bottom:none !important;
  background:#fff !important; border-radius:0 !important;
  font-family:var(--ff-d) !important; font-weight:700 !important;
  padding:.5rem 1.1rem !important; color:var(--bk) !important;
}
.stTabs [aria-selected="true"] {
  background:var(--yw) !important;
  box-shadow:3px -3px 0 var(--bk) !important;
}
.stTabs [data-baseweb="tab-panel"] {
  border:var(--bd) !important; border-top:none !important;
  padding:1.5rem !important; background:#fff !important;
  box-shadow:var(--sh) !important;
}

/* ── Alerts ── */
.stSuccess { border:var(--bd) !important; border-radius:0 !important; border-left:5px solid var(--gn) !important; }
.stInfo    { border:var(--bd) !important; border-radius:0 !important; border-left:5px solid var(--bl) !important; }
.stWarning { border:var(--bd) !important; border-radius:0 !important; border-left:5px solid var(--yw) !important; }
.stError   { border:var(--bd) !important; border-radius:0 !important; border-left:5px solid var(--rd) !important; }

/* ── Metrics ── */
[data-testid="stMetric"] {
  border:var(--bd) !important; padding:.8rem 1rem !important;
  box-shadow:var(--sh) !important; background:#fff !important;
}
[data-testid="stMetricValue"] { font-family:var(--ff-d) !important; font-weight:800 !important; }
[data-testid="stMetricLabel"] { font-family:var(--ff-m) !important; }

/* ── HR ── */
hr { border:1.5px solid var(--bk) !important; margin:1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── HEADER BANNER ────────────────────────────────────────────────────────────

st.markdown("""
<div style="background:#FFE500;border:2.5px solid #0D0D0D;box-shadow:6px 6px 0 #0D0D0D;
            padding:2rem 2.5rem;margin-bottom:2rem;position:relative;overflow:hidden;">
  <div style="position:absolute;top:-25px;right:-25px;width:110px;height:110px;
              background:#FF3B00;border:2.5px solid #0D0D0D;transform:rotate(20deg);opacity:.45;"></div>
  <div style="position:absolute;bottom:-30px;left:240px;width:75px;height:75px;
              background:#00C4FF;border:2.5px solid #0D0D0D;transform:rotate(-12deg);opacity:.4;"></div>
  <div style="position:absolute;top:15px;right:140px;width:45px;height:45px;
              background:#0D0D0D;transform:rotate(8deg);opacity:.15;"></div>
  <span style="font-family:'IBM Plex Mono',monospace;font-size:.68rem;font-weight:700;
               background:#0D0D0D;color:#FFE500;padding:.15rem .6rem;letter-spacing:.15em;">
    GEMINI 2.5 FLASH ▸ MULTI-CHAIN AI ▸ PYDANTIC OUTPUT
  </span>
  <div style="font-family:'Space Grotesk',sans-serif;font-size:2.7rem;font-weight:900;
              color:#0D0D0D;margin:.4rem 0 0;line-height:1;letter-spacing:-.04em;">
    📺 YT CONTENT<br>PLANNER PRO
  </div>
  <div style="font-family:'IBM Plex Mono',monospace;font-size:.8rem;color:#0D0D0D;
              margin:.8rem 0 0;opacity:.7;">
    Ideas → Script → Hooks → Strategy → Export. All in one shot.
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
        'letter-spacing:.15em;color:#FFE500;margin-bottom:.4rem;">▶ API CONFIG</p>',
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
    <div style="font-family:'IBM Plex Mono',monospace;font-size:.7rem;color:#FAFAF0;line-height:1.9;">
      <p style="letter-spacing:.12em;color:#FFE500;margin-bottom:.5rem;">▶ WORKFLOW</p>
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
    <div style="font-family:'IBM Plex Mono',monospace;font-size:.65rem;color:#FAFAF0;opacity:.45;line-height:1.6;">
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

def badge(label: str, bg: str = "#0D0D0D", fg: str = "#FFE500") -> str:
    return (
        f'<span style="font-family:\'IBM Plex Mono\',monospace;font-size:.68rem;'
        f'font-weight:700;letter-spacing:.14em;background:{bg};color:{fg};'
        f'padding:.15rem .55rem;">{label}</span>'
    )

def section_card(step_label: str, step_bg: str, step_fg: str, title: str, subtitle: str = "") -> str:
    sub = (
        f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:.76rem;'
        f'color:#0D0D0D;opacity:.6;margin-top:.3rem;">{subtitle}</div>'
        if subtitle else ""
    )
    return (
        f'<div style="border:2.5px solid #0D0D0D;box-shadow:5px 5px 0 #0D0D0D;'
        f'padding:1.5rem;background:#fff;margin-bottom:1rem;">'
        f'{badge(step_label, step_bg, step_fg)}'
        f'<div style="font-family:\'Space Grotesk\',sans-serif;font-weight:800;'
        f'font-size:1.3rem;margin:.7rem 0 0;color:#0D0D0D;">{title}</div>'
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

st.markdown(section_card("STEP 01 / INPUT", "#0D0D0D", "#FFE500", "What are we creating today?"),
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
        "STEP 02 / CONTENT PLAN", "#FF3B00", "#fff",
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

        # Alternating card colors for visual rhythm
        CARD_BG  = ["#FFE500","#00C4FF","#FAFAF0","#FFE500","#FF3B00",
                    "#FAFAF0","#00C4FF","#FFE500","#FAFAF0","#00C4FF"]
        CARD_FG  = ["#0D0D0D","#0D0D0D","#0D0D0D","#0D0D0D","#FFFFFF",
                    "#0D0D0D","#0D0D0D","#0D0D0D","#0D0D0D","#0D0D0D"]

        col_a, col_b = st.columns(2)
        for i, idea in enumerate(plan.video_ideas):
            with (col_a if i % 2 == 0 else col_b):
                bg, fg = CARD_BG[i], CARD_FG[i]
                st.markdown(f"""
                <div style="border:2.5px solid #0D0D0D;box-shadow:4px 4px 0 #0D0D0D;
                            padding:1rem;margin-bottom:.8rem;background:{bg};">
                  <span style="font-family:'IBM Plex Mono',monospace;font-size:.62rem;
                               opacity:.55;color:{fg};">IDEA #{i+1:02d}</span>
                  <p style="font-family:'Space Grotesk',sans-serif;font-weight:700;
                            font-size:.95rem;margin:.3rem 0 .4rem;color:{fg};">{idea.title}</p>
                  <p style="font-family:'IBM Plex Mono',monospace;font-size:.75rem;
                            color:{fg};margin:0;opacity:.8;">{idea.description}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🔍 SEO-Friendly Titles")
        for t in plan.seo_titles:
            st.markdown(f"""
            <div style="border:2px solid #0D0D0D;padding:.65rem 1rem;margin-bottom:.45rem;
                        background:#FAFAF0;box-shadow:3px 3px 0 #0D0D0D;
                        font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:.92rem;">
              🎯 {t}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📝 Ready-to-Use Description")
        st.markdown(f"""
        <div style="border:2.5px solid #0D0D0D;padding:1rem 1.2rem;background:#F0FFF4;
                    box-shadow:4px 4px 0 #0D0D0D;font-family:'IBM Plex Mono',monospace;
                    font-size:.82rem;line-height:1.8;color:#0D0D0D;">
          {plan.description}
        </div>
        """, unsafe_allow_html=True)

    # ── TAB 2: VISUALS & SEO ──────────────────────────────────────────────────
    with tab2:
        c_th, c_ht = st.columns([1, 1])

        with c_th:
            st.markdown("### 🎨 Thumbnail Mockup Preview")
            st.markdown(f"""
            <div style="border:2.5px solid #0D0D0D;box-shadow:5px 5px 0 #0D0D0D;overflow:hidden;">
              <div style="background:#FF3B00;padding:2.5rem 1.5rem;text-align:center;
                          border-bottom:2.5px solid #0D0D0D;min-height:130px;
                          display:flex;align-items:center;justify-content:center;">
                <span style="font-family:'Space Grotesk',sans-serif;font-size:1.65rem;
                             font-weight:900;color:#FFE500;text-transform:uppercase;
                             line-height:1.1;text-shadow:3px 3px 0 #0D0D0D;
                             letter-spacing:-.02em;">{plan.thumbnail.text_overlay}</span>
              </div>
              <div style="background:#FAFAF0;padding:1rem 1.2rem;">
                <div style="margin-bottom:.6rem;">
                  <span style="font-family:'IBM Plex Mono',monospace;font-size:.6rem;
                               opacity:.5;display:block;margin-bottom:.2rem;">VISUAL CONCEPT</span>
                  <span style="font-family:'Space Grotesk',sans-serif;font-size:.88rem;
                               font-weight:600;">{plan.thumbnail.visual_concept}</span>
                </div>
                <div>
                  <span style="font-family:'IBM Plex Mono',monospace;font-size:.6rem;
                               opacity:.5;display:block;margin-bottom:.2rem;">MOOD &amp; PALETTE</span>
                  <span style="font-family:'Space Grotesk',sans-serif;font-size:.88rem;
                               font-weight:600;">{plan.thumbnail.mood}</span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        with c_ht:
            st.markdown("### # Hashtag Cloud")
            tags_html = "".join([
                f'<span style="display:inline-block;border:2px solid #0D0D0D;'
                f'background:{"#FFE500" if i%3==0 else "#00C4FF" if i%3==1 else "#FF3B00"};'
                f'color:{"#0D0D0D" if i%3 < 2 else "#fff"};'
                f'font-family:\'IBM Plex Mono\',monospace;font-size:.72rem;font-weight:700;'
                f'padding:.28rem .65rem;margin:.22rem;box-shadow:2px 2px 0 #0D0D0D;">{tag}</span>'
                for i, tag in enumerate(plan.hashtags)
            ])
            st.markdown(f"""
            <div style="border:2.5px solid #0D0D0D;padding:1rem;background:#FAFAF0;
                        box-shadow:4px 4px 0 #0D0D0D;line-height:2.3;">
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
            <div style="border:2.5px solid #0D0D0D;padding:1.4rem;box-shadow:5px 5px 0 #0D0D0D;
                        background:#FFE500;margin-bottom:1rem;">
              <span style="font-family:'IBM Plex Mono',monospace;font-size:.6rem;opacity:.6;
                           display:block;margin-bottom:.4rem;">BEST DAYS TO UPLOAD</span>
              <span style="font-family:'Space Grotesk',sans-serif;font-size:1.2rem;
                           font-weight:800;">{days_display}</span>
            </div>
            <div style="border:2.5px solid #0D0D0D;padding:1.4rem;box-shadow:5px 5px 0 #0D0D0D;
                        background:#00C4FF;">
              <span style="font-family:'IBM Plex Mono',monospace;font-size:.6rem;opacity:.6;
                           display:block;margin-bottom:.4rem;">OPTIMAL UPLOAD TIME</span>
              <span style="font-family:'Space Grotesk',sans-serif;font-size:1.2rem;
                           font-weight:800;">{plan.upload_time}</span>
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
        "STEP 03 / DEEP-DIVE", "#00C4FF", "#0D0D0D",
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
        <div style="border:2.5px solid #0D0D0D;padding:1.5rem;margin:1rem 0;
                    background:#fff;box-shadow:5px 5px 0 #0D0D0D;">
          {badge("SCRIPT OUTLINE", "#0D0D0D", "#FFE500")}
          <div style="font-family:'Space Grotesk',sans-serif;font-weight:800;font-size:1.25rem;
                      margin:.5rem 0 .2rem;color:#0D0D0D;">{script.video_title}</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:.73rem;
                      color:#0D0D0D;opacity:.5;">Duration: {script.total_duration}</div>
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

            HOOK_BG = {"Visual": "#FFE500", "Verbal": "#00C4FF", "Text-on-Screen": "#FF3B00"}
            HOOK_FG = {"Visual": "#0D0D0D", "Verbal": "#0D0D0D", "Text-on-Screen": "#FFFFFF"}

            for hook in script.hooks:
                bg = HOOK_BG.get(hook.hook_type, "#FAFAF0")
                fg = HOOK_FG.get(hook.hook_type, "#0D0D0D")
                st.markdown(f"""
                <div style="border:2.5px solid #0D0D0D;box-shadow:4px 4px 0 #0D0D0D;
                            margin-bottom:1rem;overflow:hidden;">
                  <div style="background:{bg};padding:.5rem 1rem;border-bottom:2px solid #0D0D0D;">
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:.68rem;
                                 font-weight:700;color:{fg};letter-spacing:.12em;">
                      {hook.hook_type.upper()} HOOK
                    </span>
                  </div>
                  <div style="padding:1rem;background:#FAFAF0;">
                    <p style="font-family:'Space Grotesk',sans-serif;font-weight:700;
                              font-size:1rem;margin:0 0 .5rem;color:#0D0D0D;">
                      "{hook.hook_text}"
                    </p>
                    <p style="font-family:'IBM Plex Mono',monospace;font-size:.75rem;
                              color:#0D0D0D;opacity:.65;margin:0;">
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
                    f'<div style="margin-top:.5rem;background:#FFE500;padding:.25rem .6rem;'
                    f'display:inline-block;border:1.5px solid #0D0D0D;'
                    f'font-family:\'IBM Plex Mono\',monospace;font-size:.68rem;font-weight:700;">'
                    f'📣 CTA: {sec.cta}</div>'
                ) if sec.cta else ""

                st.markdown(f"""
                <div style="border:2px solid #0D0D0D;margin-bottom:.75rem;
                            overflow:hidden;box-shadow:3px 3px 0 #0D0D0D;">
                  <div style="background:#0D0D0D;padding:.45rem 1rem;
                              display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-family:'Space Grotesk',sans-serif;font-weight:700;
                                 color:#FFE500;font-size:.9rem;">{sec.section_title}</span>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:.68rem;
                                 color:#FAFAF0;opacity:.6;">{sec.timestamp}</span>
                  </div>
                  <div style="padding:.85rem 1rem;background:#FAFAF0;">
                    <p style="font-family:'IBM Plex Mono',monospace;font-size:.8rem;
                              color:#0D0D0D;margin:0 0 .4rem;">{sec.content_notes}</p>
                    <p style="font-family:'IBM Plex Mono',monospace;font-size:.7rem;
                              color:#0D0D0D;opacity:.55;margin:0;">🎬 B-roll: {sec.broll_cue}</p>
                    {cta_block}
                  </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="border:2.5px solid #0D0D0D;padding:1rem 1.2rem;background:#FF3B00;
                        box-shadow:4px 4px 0 #0D0D0D;margin-top:1rem;">
              <span style="font-family:'IBM Plex Mono',monospace;font-size:.6rem;
                           color:#fff;opacity:.7;display:block;margin-bottom:.3rem;">CLOSING CTA</span>
              <span style="font-family:'Space Grotesk',sans-serif;font-weight:700;
                           font-size:1rem;color:#fff;">{script.closing_cta}</span>
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
            opacity:.38;padding:.8rem 0;color:#0D0D0D;">
  YT CONTENT PLANNER PRO · STREAMLIT + LANGCHAIN + GEMINI 2.5 FLASH
</div>
""", unsafe_allow_html=True)
