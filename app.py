# ===================== STEP 1: LOAD MODULES =====================

import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ===================== STEP 2: PAGE CONFIG =====================

st.set_page_config(
    page_title="AI YouTube Content Planner",
    page_icon="📺",
    layout="wide"
)

st.title("📺 AI YouTube Content Planner")
st.write("Generate YouTube video ideas, SEO titles, thumbnail suggestions and upload schedule using AI.")


# ===================== STEP 3: API KEY =====================

st.sidebar.title("SET API CONFIG")

GOOGLE_API_KEY = st.sidebar.text_input(
    "GOOGLE API KEY",
    type="password"
)

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

if GOOGLE_API_KEY:
    st.sidebar.success("API Key Loaded!!")
else:
    st.sidebar.info("Enter your Google API Key")


# ===================== STEP 4: GET USER INPUT =====================

st.subheader("Enter Content Details")

topic = st.text_input(
    "Enter YouTube Topic",
    placeholder="Example: Artificial Intelligence"
)

niche = st.selectbox(
    "Select Your Niche",
    [
        "Education",
        "Technology",
        "Motivation",
        "Gaming",
        "Fitness",
        "Finance",
        "Entertainment",
        "Travel",
        "Food",
        "Other"
    ]
)

target_audience = st.selectbox(
    "Select Target Audience",
    [
        "Global",
        "India",
        "USA",
        "UK",
        "Students",
        "Working Professionals",
        "General Audience"
    ]
)


# ===================== STEP 5: CREATE PROMPT =====================

prompt = ChatPromptTemplate.from_template("""
You are a YouTube Content Planning Assistant.

Create a simple and useful YouTube content plan based on the
information provided by the user.

Topic: {topic}

Niche: {niche}

Target Audience: {target_audience}


Generate the content plan in the following format:


1. VIDEO IDEAS

Generate 10 interesting YouTube video ideas related to the topic.


2. SEO FRIENDLY TITLES

Generate 5 attractive and SEO-friendly YouTube titles.


3. VIDEO DESCRIPTION

Write one short and engaging YouTube video description.


4. HASHTAGS

Generate 10 relevant YouTube hashtags.


5. THUMBNAIL SUGGESTION

Suggest one simple thumbnail idea.

Mention:
- Thumbnail text
- Image or visual idea


6. UPLOAD SCHEDULE

Suggest:
- Best days to upload
- Suitable upload time

Keep the answer simple, clear and properly formatted.
""")


# ===================== STEP 6: LOAD GEMINI MODEL =====================

if GOOGLE_API_KEY:

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY
    )

    parser = StrOutputParser()


    # ===================== STEP 7: CREATE LCEL CHAIN =====================

    youtube_chain = prompt | llm | parser


    # ===================== STEP 8: GENERATE CONTENT =====================

    if st.button("Generate Content Plan"):

        if topic:

            with st.spinner("Generating YouTube Content Plan..."):

                try:

                    response = youtube_chain.invoke({
                        "topic": topic,
                        "niche": niche,
                        "target_audience": target_audience
                    })

                    st.success("Content Plan Generated!")

                    st.subheader("📋 Your YouTube Content Plan")

                    st.markdown(response)

                except Exception as e:

                    st.error("Something went wrong!")
                    st.write(e)

        else:

            st.warning("Please enter a YouTube topic.")

else:

    st.info("👈 Please enter your Google API Key in the sidebar.")
