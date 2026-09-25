
import streamlit as st
import requests
import os
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="YouTube RAG",
    page_icon="▶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

FASTAPI_URL = os.getenv(
    "FASTAPI_URL",
    "http://localhost:8000"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       COLOR SYSTEM
       ======================================================== */

    :root {

        --bg: #F8FAFC;

        --card: #FFFFFF;

        --text: #0F172A;

        --text-secondary: #64748B;

        --text-muted: #94A3B8;

        --border: #E2E8F0;

        /* Professional Blue */
        --accent: #2563EB;

        --accent-hover: #1D4ED8;

        --accent-light: #EFF6FF;

        --accent-border: #DBEAFE;

        /* Success */
        --success: #16A34A;

        --success-bg: #F0FDF4;

        --success-border: #DCFCE7;
    }


    /* ========================================================
       GLOBAL APP
       ======================================================== */

    .stApp {

        background: var(--bg);

        color: var(--text);
    }


    /* ========================================================
       MAIN CONTAINER
       ======================================================== */

    .block-container {

        max-width: 1100px;

        padding-top: 1.5rem;

        padding-bottom: 3rem;

        padding-left: 2rem;

        padding-right: 2rem;
    }


    /* ========================================================
       GENERAL STREAMLIT SPACING
       ======================================================== */

    div[data-testid="stVerticalBlock"] {

        gap: 0.6rem;
    }


    /* ========================================================
       NAVIGATION
       ======================================================== */

    .navbar {

        display: flex;

        align-items: center;

        justify-content: space-between;

        padding: 8px 0 22px 0;

        border-bottom: 1px solid var(--border);

        margin-bottom: 35px;
    }


    .brand {

        display: flex;

        align-items: center;

        gap: 10px;

        color: var(--text);

        font-size: 17px;

        font-weight: 700;

        letter-spacing: -0.2px;
    }


    .brand-icon {

        width: 31px;

        height: 31px;

        display: flex;

        align-items: center;

        justify-content: center;

        border-radius: 8px;

        background: var(--accent-light);

        color: var(--accent);

        font-size: 14px;

        font-weight: 800;
    }


    .nav-links {

        display: flex;

        align-items: center;

        gap: 24px;

        color: var(--text-secondary);

        font-size: 13px;

        font-weight: 500;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {

        text-align: center;

        padding-top: 45px;

        padding-bottom: 25px;
    }


    .hero-eyebrow {

        display: inline-flex;

        align-items: center;

        padding: 6px 11px;

        border: 1px solid var(--accent-border);

        border-radius: 999px;

        background: var(--accent-light);

        color: var(--accent);

        font-size: 12px;

        font-weight: 600;

        margin-bottom: 18px;
    }


    .hero-title {

        max-width: 780px;

        margin: 0 auto;

        color: var(--text);

        font-size: 48px;

        line-height: 1.08;

        letter-spacing: -1.8px;

        font-weight: 750;
    }


    .hero-subtitle {

        max-width: 650px;

        margin: 18px auto 0 auto;

        color: var(--text-secondary);

        font-size: 16px;

        line-height: 1.7;
    }


    /* ========================================================
       URL CARD
       ======================================================== */

    .url-card {

        max-width: 850px;

        margin: 35px auto 0 auto;

        padding: 24px;

        background: var(--card);

        border: 1px solid var(--border);

        border-radius: 14px;

        box-shadow:
            0 8px 24px rgba(15, 23, 42, 0.05);
    }


    .url-label {

        margin-bottom: 9px;

        color: var(--text);

        font-size: 13px;

        font-weight: 650;
    }


    .url-description {

        margin-bottom: 14px;

        color: var(--text-secondary);

        font-size: 12px;
    }


    /* ========================================================
       TEXT INPUT
       ======================================================== */

    div[data-baseweb="input"] {

        background: var(--card);

        border: 1px solid var(--border);

        border-radius: 9px;

        transition:
            border-color 0.15s ease,
            box-shadow 0.15s ease;
    }


    div[data-baseweb="input"]:hover {

        border-color: #CBD5E1;
    }


    div[data-baseweb="input"]:focus-within {

        border-color: var(--accent);

        box-shadow:
            0 0 0 3px rgba(37, 99, 235, 0.08);
    }


    input {

        color: var(--text) !important;
    }


    input::placeholder {

        color: var(--text-muted) !important;
    }


    /* ========================================================
       PRIMARY BUTTON
       ======================================================== */

    .stButton > button {

        min-height: 44px;

        border-radius: 9px;

        border: 1px solid var(--accent);

        background: var(--accent);

        color: #FFFFFF;

        font-size: 13px;

        font-weight: 650;

        transition:
            background 0.15s ease,
            border-color 0.15s ease,
            transform 0.15s ease;
    }


    .stButton > button:hover {

        background: var(--accent-hover);

        border-color: var(--accent-hover);

        color: #FFFFFF;

        transform: translateY(-1px);
    }


    .stButton > button:active {

        transform: translateY(0);
    }


    /* ========================================================
       CAPABILITIES
       ======================================================== */

    .capabilities {

        max-width: 850px;

        margin: 22px auto 0 auto;
    }


    .capability {

        display: flex;

        align-items: center;

        justify-content: center;

        gap: 7px;

        color: var(--text-secondary);

        font-size: 12px;
    }


    .capability-check {

        color: var(--success);

        font-weight: 700;
    }


    /* ========================================================
       SECTION TITLE
       ======================================================== */

    .section-title {

        margin-top: 80px;

        margin-bottom: 7px;

        text-align: center;

        color: var(--text);

        font-size: 22px;

        font-weight: 700;

        letter-spacing: -0.4px;
    }


    .section-subtitle {

        text-align: center;

        color: var(--text-secondary);

        font-size: 13px;

        margin-bottom: 24px;
    }


    /* ========================================================
       FEATURE CARDS
       ======================================================== */

    .feature-card {

        height: 100%;

        min-height: 175px;

        padding: 22px;

        background: var(--card);

        border: 1px solid var(--border);

        border-radius: 12px;

        transition:
            border-color 0.15s ease,
            box-shadow 0.15s ease;
    }


    .feature-card:hover {

        border-color: #CBD5E1;

        box-shadow:
            0 5px 16px rgba(15, 23, 42, 0.05);
    }


    .feature-number {

        margin-bottom: 17px;

        color: var(--accent);

        font-size: 12px;

        font-weight: 700;

        letter-spacing: 0.5px;
    }


    .feature-title {

        margin-bottom: 8px;

        color: var(--text);

        font-size: 15px;

        font-weight: 650;
    }


    .feature-description {

        color: var(--text-secondary);

        font-size: 13px;

        line-height: 1.65;
    }


    /* ========================================================
       LOADING
       ======================================================== */

    .loading-card {

        max-width: 650px;

        margin: 70px auto;

        padding: 35px;

        text-align: center;

        background: var(--card);

        border: 1px solid var(--border);

        border-radius: 14px;
    }


    .loader {

        width: 38px;

        height: 38px;

        margin: 0 auto 20px auto;

        border-radius: 50%;

        border: 3px solid var(--accent-border);

        border-top-color: var(--accent);

        animation: spin 0.8s linear infinite;
    }


    @keyframes spin {

        to {
            transform: rotate(360deg);
        }
    }


    .loading-title {

        color: var(--text);

        font-size: 19px;

        font-weight: 700;

        margin-bottom: 7px;
    }


    .loading-description {

        color: var(--text-secondary);

        font-size: 13px;

        line-height: 1.6;
    }


    /* ========================================================
       CHAT HEADER
       ======================================================== */

    .chat-header {

        display: flex;

        align-items: center;

        justify-content: space-between;

        padding: 17px 20px;

        margin-bottom: 22px;

        background: var(--card);

        border: 1px solid var(--border);

        border-radius: 12px;

        box-shadow:
            0 4px 14px rgba(15, 23, 42, 0.035);
    }


    .chat-brand {

        display: flex;

        align-items: center;

        gap: 11px;
    }


    .chat-icon {

        width: 36px;

        height: 36px;

        display: flex;

        align-items: center;

        justify-content: center;

        border-radius: 9px;

        background: var(--accent-light);

        color: var(--accent);

        font-size: 15px;

        font-weight: 700;
    }


    .chat-title {

        color: var(--text);

        font-size: 15px;

        font-weight: 700;
    }


    .chat-video-id {

        margin-top: 3px;

        color: var(--text-muted);

        font-size: 11px;
    }


    .ready-status {

        display: flex;

        align-items: center;

        gap: 7px;

        padding: 6px 10px;

        border-radius: 999px;

        background: var(--success-bg);

        border: 1px solid var(--success-border);

        color: var(--success);

        font-size: 11px;

        font-weight: 600;
    }


    .ready-dot {

        width: 6px;

        height: 6px;

        border-radius: 50%;

        background: var(--success);
    }


    /* ========================================================
       EMPTY CHAT
       ======================================================== */

    .chat-empty {

        max-width: 650px;

        margin: 80px auto;

        text-align: center;
    }


    .chat-empty-icon {

        width: 52px;

        height: 52px;

        margin: 0 auto 18px auto;

        display: flex;

        align-items: center;

        justify-content: center;

        border-radius: 14px;

        background: var(--accent-light);

        color: var(--accent);

        font-size: 20px;

        font-weight: 700;
    }


    .chat-empty-title {

        color: var(--text);

        font-size: 21px;

        font-weight: 700;

        margin-bottom: 8px;
    }


    .chat-empty-text {

        max-width: 560px;

        margin: 0 auto;

        color: var(--text-secondary);

        font-size: 13px;

        line-height: 1.7;
    }


    /* ========================================================
       CHAT MESSAGES
       ======================================================== */

    [data-testid="stChatMessage"] {

        border-radius: 12px !important;

        border: 1px solid var(--border);

        margin-bottom: 10px;

        padding: 7px 13px;
    }


    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {

        background: var(--accent-light);
    }


    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {

        background: var(--card);
    }


    /* ========================================================
       CHAT INPUT
       ======================================================== */

    [data-testid="stChatInput"] {

        background: var(--card);

        border: 1px solid var(--border);

        border-radius: 12px;

        box-shadow:
            0 5px 20px rgba(15, 23, 42, 0.06);
    }


    [data-testid="stChatInput"]:focus-within {

        border-color: var(--accent);

        box-shadow:
            0 0 0 3px rgba(37, 99, 235, 0.08);
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    [data-testid="stAlert"] {

        border-radius: 9px;
    }


    /* ========================================================
       PROGRESS BAR
       ======================================================== */

    [data-testid="stProgressBar"] > div > div {

        background: var(--accent);
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {

        margin-top: 65px;

        padding-top: 20px;

        border-top: 1px solid var(--border);

        text-align: center;

        color: var(--text-muted);

        font-size: 11px;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .block-container {

            padding-left: 1rem;

            padding-right: 1rem;
        }


        .hero {

            padding-top: 25px;
        }


        .hero-title {

            font-size: 36px;

            letter-spacing: -1.2px;
        }


        .hero-subtitle {

            font-size: 14px;
        }


        .url-card {

            padding: 18px;
        }


        .nav-links {

            display: none;
        }


        .ready-status {

            display: none;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "stage" not in st.session_state:
    st.session_state.stage = "url"


if "video_id" not in st.session_state:
    st.session_state.video_id = None


if "youtube_url" not in st.session_state:
    st.session_state.youtube_url = None


if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# FASTAPI FUNCTIONS
# ============================================================

def prepare_video(youtube_url):

    try:

        response = requests.get(
            f"{FASTAPI_URL}/Youtube_url",

            params={
                "url": youtube_url
            },

            timeout=600
        )


        if response.status_code != 200:

            try:

                error = response.json()

            except Exception:

                error = response.text

            return False, error


        data = response.json()


        if data.get("status") != "ready":

            return False, (
                "Backend did not return a ready status."
            )


        return True, data


    except requests.exceptions.ConnectionError:

        return False, (
            "Could not connect to FastAPI. "
            "Make sure the FastAPI server is running."
        )


    except requests.exceptions.Timeout:

        return False, (
            "The request timed out while "
            "preparing the video."
        )


    except Exception as e:

        return False, str(e)


# ============================================================

def ask_question(question):

    try:

        response = requests.post(

            f"{FASTAPI_URL}/ask",

            json={
                "question": question
            },

            timeout=600
        )


        if response.status_code != 200:

            return False, response.text


        data = response.json()


        if "answer" in data:

            return True, data["answer"]


        return False, data.get(
            "error",
            "Unknown backend error."
        )


    except requests.exceptions.ConnectionError:

        return False, (
            "Could not connect to FastAPI."
        )


    except requests.exceptions.Timeout:

        return False, (
            "The request timed out."
        )


    except Exception as e:

        return False, str(e)


# ============================================================

def reset_app():

    st.session_state.stage = "url"

    st.session_state.video_id = None

    st.session_state.youtube_url = None

    st.session_state.messages = []


# ============================================================
# NAVBAR
# ============================================================

st.markdown(
    """
    <div class="navbar">

        <div class="brand">

            <div class="brand-icon">
                ▶
            </div>

            YouTube RAG

        </div>


        <div class="nav-links">

            <span>
                AI Video Intelligence
            </span>

            <span>
                RAG System
            </span>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LANDING PAGE
# ============================================================

if st.session_state.stage == "url":


    # ========================================================
    # HERO
    # ========================================================

    st.markdown(
        """
        <div class="hero">

            <div class="hero-eyebrow">
                AI-powered video understanding
            </div>


            <div class="hero-title">
                Understand any YouTube video.
            </div>


            <div class="hero-subtitle">
                Ask questions and get answers grounded
                in the video's actual content using
                retrieval-augmented generation.
            </div>

        </div>
        """,

        unsafe_allow_html=True
    )


    # ========================================================
    # URL CARD
    # ========================================================

    st.markdown(
        """
        <div class="url-card">

            <div class="url-label">
                YouTube video
            </div>


            <div class="url-description">
                Paste a public YouTube URL to build
                a searchable knowledge base.
            </div>

        </div>
        """,

        unsafe_allow_html=True
    )


    # ========================================================
    # URL INPUT
    # ========================================================

    youtube_url = st.text_input(

        "YouTube URL",

        placeholder=
        "https://www.youtube.com/watch?v=...",

        label_visibility="collapsed"
    )


    # ========================================================
    # ANALYZE BUTTON
    # ========================================================

    button_left, button_center, button_right = st.columns(
        [2, 2, 2]
    )


    with button_center:

        analyze_button = st.button(

            "Analyze video",

            use_container_width=True
        )


    # ========================================================
    # CAPABILITIES
    # ========================================================

    st.markdown(
        """
        <div class="capabilities">

            <div style="
                display:flex;
                justify-content:center;
                gap:28px;
                flex-wrap:wrap;
            ">

                <div class="capability">
                    <span class="capability-check">✓</span>
                    Transcript retrieval
                </div>


                <div class="capability">
                    <span class="capability-check">✓</span>
                    Semantic search
                </div>


                <div class="capability">
                    <span class="capability-check">✓</span>
                    Hybrid retrieval
                </div>


                <div class="capability">
                    <span class="capability-check">✓</span>
                    Context-grounded answers
                </div>

            </div>

        </div>
        """,

        unsafe_allow_html=True
    )


    # ========================================================
    # PROCESS VIDEO
    # ========================================================

    if analyze_button:

        youtube_url = youtube_url.strip()


        # ----------------------------------------------------
        # VALIDATE URL
        # ----------------------------------------------------

        if not youtube_url:

            st.error(
                "Please enter a YouTube URL."
            )

            st.stop()


        if (
            "youtube.com" not in youtube_url
            and
            "youtu.be" not in youtube_url
        ):

            st.error(
                "Please enter a valid YouTube URL."
            )

            st.stop()


        # ----------------------------------------------------
        # SAVE URL
        # ----------------------------------------------------

        st.session_state.youtube_url = youtube_url


        # ----------------------------------------------------
        # LOADING
        # ----------------------------------------------------

        loading_placeholder = st.empty()


        with loading_placeholder.container():

            st.markdown(
                """
                <div class="loading-card">

                    <div class="loader"></div>


                    <div class="loading-title">
                        Preparing your video
                    </div>


                    <div class="loading-description">
                        The RAG pipeline is processing
                        the video and preparing it for
                        question answering.
                    </div>

                </div>
                """,

                unsafe_allow_html=True
            )


            progress = st.progress(

                0,

                text=
                "Connecting to the RAG backend..."
            )


            progress.progress(

                20,

                text=
                "Connecting to FastAPI..."
            )


            # ------------------------------------------------
            # CALL FASTAPI
            # ------------------------------------------------

            success, result = prepare_video(
                youtube_url
            )


            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            if success:

                progress.progress(

                    100,

                    text=
                    "Video ready."
                )


                st.session_state.video_id = (

                    result["video_id"]

                )


                st.session_state.stage = "chat"


                st.session_state.messages = []


                st.rerun()


            # ------------------------------------------------
            # ERROR
            # ------------------------------------------------

            else:

                progress.empty()


                st.error(
                    f"Failed to prepare video: {result}"
                )


    # ========================================================
    # HOW IT WORKS
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            How it works
        </div>


        <div class="section-subtitle">
            From YouTube URL to conversational knowledge.
        </div>
        """,

        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    # ========================================================
    # STEP 01
    # ========================================================

    with col1:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-number">
                    01
                </div>


                <div class="feature-title">
                    Video ingestion
                </div>


                <div class="feature-description">
                    The system retrieves the video's
                    transcript and prepares the content
                    for semantic processing.
                </div>

            </div>
            """,

            unsafe_allow_html=True
        )


    # ========================================================
    # STEP 02
    # ========================================================

    with col2:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-number">
                    02
                </div>


                <div class="feature-title">
                    Intelligent retrieval
                </div>


                <div class="feature-description">
                    Relevant chunks are retrieved using
                    semantic and keyword-based retrieval,
                    followed by reranking.
                </div>

            </div>
            """,

            unsafe_allow_html=True
        )


    # ========================================================
    # STEP 03
    # ========================================================

    with col3:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-number">
                    03
                </div>


                <div class="feature-title">
                    Grounded answer
                </div>


                <div class="feature-description">
                    The language model generates an answer
                    using the retrieved context from
                    the video's content.
                </div>

            </div>
            """,

            unsafe_allow_html=True
        )


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        """
        <div class="footer">
            YouTube RAG · Retrieval-Augmented Video Intelligence
        </div>
        """,

        unsafe_allow_html=True
    )


# ============================================================
# CHAT PAGE
# ============================================================

elif st.session_state.stage == "chat":


    # ========================================================
    # CHAT HEADER
    # ========================================================

    header_left, header_right = st.columns(
        [5, 1]
    )


    with header_left:

        st.markdown(
            f"""
            <div class="chat-header">

                <div class="chat-brand">

                    <div class="chat-icon">
                        ▶
                    </div>


                    <div>

                        <div class="chat-title">
                            YouTube RAG
                        </div>


                        <div class="chat-video-id">
                            Video ID:
                            {st.session_state.video_id}
                        </div>

                    </div>

                </div>


                <div class="ready-status">

                    <span class="ready-dot"></span>

                    RAG ready

                </div>

            </div>
            """,

            unsafe_allow_html=True
        )


    # ========================================================
    # NEW VIDEO BUTTON
    # ========================================================

    with header_right:

        if st.button(

            "New video",

            use_container_width=True
        ):

            reset_app()

            st.rerun()


    # ========================================================
    # EMPTY CHAT
    # ========================================================

    if not st.session_state.messages:

        st.markdown(
            """
            <div class="chat-empty">

                <div class="chat-empty-icon">
                    Q
                </div>


                <div class="chat-empty-title">
                    Ask about this video
                </div>


                <div class="chat-empty-text">
                    Ask about the main ideas, specific
                    concepts, explanations, comparisons,
                    examples, or any detail discussed
                    in the video.
                </div>

            </div>
            """,

            unsafe_allow_html=True
        )


    # ========================================================
    # CHAT HISTORY
    # ========================================================

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # ========================================================
    # CHAT INPUT
    # ========================================================

    question = st.chat_input(

        "Ask something about this video..."
    )


    # ========================================================
    # PROCESS QUESTION
    # ========================================================

    if question:

        question = question.strip()


        if not question:

            st.stop()


        # ----------------------------------------------------
        # SAVE USER MESSAGE
        # ----------------------------------------------------

        st.session_state.messages.append(

            {
                "role": "user",

                "content": question
            }

        )


        # ----------------------------------------------------
        # DISPLAY USER MESSAGE
        # ----------------------------------------------------

        with st.chat_message("user"):

            st.markdown(question)


        # ----------------------------------------------------
        # GENERATE ANSWER
        # ----------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "Searching the video..."
            ):

                success, answer = ask_question(
                    question
                )


            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            if success:

                st.markdown(answer)


                st.session_state.messages.append(

                    {
                        "role": "assistant",

                        "content": answer
                    }

                )


            # ------------------------------------------------
            # ERROR
            # ------------------------------------------------

            else:

                st.error(answer)


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        """
        <div class="footer">
            Answers generated from retrieved video context
        </div>
        """,

        unsafe_allow_html=True
    )

