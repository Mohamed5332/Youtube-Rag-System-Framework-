import streamlit as st
import requests
import time
import os 
from dotenv import load_dotenv

# ============================================================
# PAGE CONFIG
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="YouTube RAG",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="collapsed"
)


FASTAPI_URL = os.getenv("FASTAPI_URL", 
                        "http://localhost:8000")


st.markdown(
    """
    <style>

    /* ======================================================
       MAIN APP
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 20% 10%,
                rgba(99, 102, 241, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at 80% 20%,
                rgba(168, 85, 247, 0.10),
                transparent 30%
            ),
            #0b0f19;

        color: #f8fafc;
    }


    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }


    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        text-align: center;
        padding-top: 70px;
        padding-bottom: 30px;
    }


    .hero-badge {
        display: inline-block;

        padding: 7px 15px;

        border-radius: 999px;

        background: rgba(99, 102, 241, 0.12);

        border: 1px solid rgba(129, 140, 248, 0.25);

        color: #a5b4fc;

        font-size: 13px;

        font-weight: 600;

        margin-bottom: 20px;
    }


    .hero-title {
        font-size: 56px;

        font-weight: 800;

        letter-spacing: -2px;

        line-height: 1.05;

        margin-bottom: 20px;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #c7d2fe,
                #a78bfa
            );

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;
    }


    .hero-subtitle {
        font-size: 18px;

        color: #94a3b8;

        max-width: 650px;

        margin: auto;

        line-height: 1.7;
    }


    /* ======================================================
       URL CARD
       ====================================================== */

    .url-card {
        background: rgba(15, 23, 42, 0.72);

        border: 1px solid rgba(148, 163, 184, 0.12);

        border-radius: 24px;

        padding: 30px;

        margin-top: 35px;

        box-shadow:
            0 25px 60px rgba(0, 0, 0, 0.35);

        backdrop-filter: blur(20px);
    }


    .input-label {
        color: #cbd5e1;

        font-size: 14px;

        font-weight: 600;

        margin-bottom: 10px;
    }


    /* ======================================================
       STREAMLIT INPUT
       ====================================================== */

    div[data-baseweb="input"] {

        background:
            rgba(15, 23, 42, 0.90);

        border-radius: 12px;

        border:
            1px solid rgba(148, 163, 184, 0.18);
    }


    div[data-baseweb="input"]:focus-within {

        border-color:
            rgba(129, 140, 248, 0.65);

        box-shadow:
            0 0 0 1px
            rgba(129, 140, 248, 0.25);
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {

        border-radius: 12px;

        border:
            1px solid rgba(129, 140, 248, 0.35);

        background:
            linear-gradient(
                135deg,
                #6366f1,
                #8b5cf6
            );

        color: white;

        font-weight: 700;

        height: 48px;

        transition:
            all 0.2s ease;
    }


    .stButton > button:hover {

        transform:
            translateY(-2px);

        box-shadow:
            0 10px 30px
            rgba(99, 102, 241, 0.30);
    }


    /* ======================================================
       FEATURE CARDS
       ====================================================== */

    .feature-card {

        background:
            rgba(15, 23, 42, 0.55);

        border:
            1px solid
            rgba(148, 163, 184, 0.10);

        border-radius: 18px;

        padding: 22px;

        min-height: 175px;

        transition:
            all 0.25s ease;
    }


    .feature-card:hover {

        transform:
            translateY(-4px);

        border-color:
            rgba(129, 140, 248, 0.30);

        box-shadow:
            0 15px 35px
            rgba(0, 0, 0, 0.25);
    }


    .feature-icon {

        font-size: 28px;

        margin-bottom: 12px;
    }


    .feature-title {

        font-size: 16px;

        font-weight: 700;

        color: #f8fafc;

        margin-bottom: 7px;
    }


    .feature-text {

        font-size: 13px;

        color: #94a3b8;

        line-height: 1.6;
    }


    /* ======================================================
       LOADING
       ====================================================== */

    .loading-container {

        text-align: center;

        padding-top: 100px;

        padding-bottom: 40px;
    }


    .loader {

        width: 55px;

        height: 55px;

        margin: auto;

        border-radius: 50%;

        border:
            4px solid
            rgba(129, 140, 248, 0.15);

        border-top-color:
            #818cf8;

        animation:
            spin 0.9s linear infinite;
    }


    @keyframes spin {

        to {
            transform: rotate(360deg);
        }

    }


    .loading-title {

        font-size: 25px;

        font-weight: 750;

        color: #f8fafc;

        margin-top: 20px;
    }


    .loading-text {

        color: #94a3b8;

        font-size: 14px;

        margin-top: 8px;

        line-height: 1.6;
    }


    /* ======================================================
       CHAT HEADER
       ====================================================== */

    .chat-header {

        display: flex;

        align-items: center;

        justify-content: space-between;

        padding: 18px 22px;

        margin-bottom: 25px;

        border-radius: 18px;

        background:
            rgba(15, 23, 42, 0.75);

        border:
            1px solid
            rgba(148, 163, 184, 0.12);

        backdrop-filter:
            blur(15px);
    }


    .chat-title {

        font-size: 21px;

        font-weight: 750;

        color: #f8fafc;
    }


    .chat-status {

        font-size: 12px;

        color: #86efac;

        display: flex;

        align-items: center;

        gap: 6px;
    }


    .status-dot {

        width: 7px;

        height: 7px;

        border-radius: 50%;

        background: #22c55e;

        box-shadow:
            0 0 10px #22c55e;
    }


    .video-info {

        padding: 8px 12px;

        border-radius: 10px;

        background:
            rgba(30, 41, 59, 0.55);

        border:
            1px solid
            rgba(148, 163, 184, 0.10);

        color: #94a3b8;

        font-size: 12px;

        margin-top: 7px;
    }


    /* ======================================================
       EMPTY CHAT
       ====================================================== */

    .empty-chat {

        text-align: center;

        padding-top: 90px;

        padding-bottom: 70px;
    }


    .empty-icon {

        font-size: 55px;

        margin-bottom: 15px;
    }


    .empty-title {

        font-size: 24px;

        font-weight: 750;

        color: #f8fafc;

        margin-bottom: 8px;
    }


    .empty-text {

        color: #94a3b8;

        font-size: 14px;

        max-width: 550px;

        margin: auto;

        line-height: 1.7;
    }


    /* ======================================================
       CHAT INPUT
       ====================================================== */

    [data-testid="stChatInput"] {

        background:
            rgba(15, 23, 42, 0.85);

        border-radius: 16px;
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {

        text-align: center;

        color: #64748b;

        font-size: 12px;

        padding-top: 35px;

        padding-bottom: 10px;
    }


    /* ======================================================
       RESPONSIVE
       ====================================================== */

    @media (max-width: 768px) {

        .hero-title {

            font-size: 40px;
        }

        .hero-subtitle {

            font-size: 15px;
        }

        .hero {

            padding-top: 40px;
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
# URL PAGE
# ============================================================

if st.session_state.stage == "url":


    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.html(
        """
        <div class="hero">

            <div class="hero-badge">
                ✦ AI-Powered Video Intelligence
            </div>

            <div class="hero-title">
                Talk to Any YouTube Video
            </div>

            <div class="hero-subtitle">
                Transform a YouTube video into an intelligent
                conversational knowledge base. Ask questions,
                explore ideas, and understand the content
                through your RAG-powered AI assistant.
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # URL CARD LABEL
    # --------------------------------------------------------

    st.html(
        """
        <div class="url-card">

            <div class="input-label">
                YouTube Video URL
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # URL INPUT
    # --------------------------------------------------------

    youtube_url = st.text_input(

        "YouTube URL",

        placeholder=
        "https://www.youtube.com/watch?v=...",

        label_visibility="collapsed"
    )


    # --------------------------------------------------------
    # ANALYZE BUTTON
    # --------------------------------------------------------

    button_col1, button_col2, button_col3 = st.columns(
        [1, 2, 1]
    )


    with button_col2:

        start_button = st.button(

            "🚀 Analyze Video",

            use_container_width=True
        )


    # --------------------------------------------------------
    # PROCESS VIDEO
    # --------------------------------------------------------

    if start_button:

        youtube_url = youtube_url.strip()


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


        st.session_state.youtube_url = youtube_url


        loading_area = st.empty()


        with loading_area.container():


            st.html(
                """
                <div class="loading-container">

                    <div class="loader"></div>

                    <div class="loading-title">
                        Preparing your AI workspace
                    </div>

                    <div class="loading-text">
                        Your video is being processed.
                        This may take a little while
                        for a new video.
                    </div>

                </div>
                """
            )


            progress = st.progress(

                0,

                text=
                "Connecting to the RAG backend..."
            )


            progress.progress(

                15,

                text=
                "Connecting to FastAPI..."
            )


            time.sleep(0.2)


            progress.progress(

                30,

                text=
                "Preparing video pipeline..."
            )


            # ------------------------------------------------
            # CALL FASTAPI
            # ------------------------------------------------

            success, result = prepare_video(
                youtube_url
            )


            if success:

                progress.progress(

                    100,

                    text=
                    "AI workspace ready!"
                )


                time.sleep(0.5)


                st.session_state.video_id = (
                    result["video_id"]
                )


                st.session_state.stage = "chat"


                st.session_state.messages = []


                st.rerun()


            else:

                progress.empty()


                st.error(
                    f"Failed to prepare video: {result}"
                )


    # --------------------------------------------------------
    # SPACE
    # --------------------------------------------------------

    st.html(
        "<div style='height: 20px;'></div>"
    )


    # --------------------------------------------------------
    # FEATURE CARDS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    # ========================================================
    # CARD 1
    # ========================================================

    with col1:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🧠
                </div>

                <div class="feature-title">
                    Semantic Understanding
                </div>

                <div class="feature-text">
                    Ask natural-language questions
                    and retrieve the most relevant
                    information from the video's
                    content.
                </div>

            </div>
            """
        )


    # ========================================================
    # CARD 2
    # ========================================================

    with col2:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🔎
                </div>

                <div class="feature-title">
                    Hybrid Retrieval
                </div>

                <div class="feature-text">
                    Your backend combines semantic
                    retrieval and keyword-based
                    retrieval to improve contextual
                    search.
                </div>

            </div>
            """
        )


    # ========================================================
    # CARD 3
    # ========================================================

    with col3:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    💬
                </div>

                <div class="feature-title">
                    Conversational AI
                </div>

                <div class="feature-text">
                    Continue asking questions and
                    explore the video naturally
                    through an interactive AI chat
                    interface.
                </div>

            </div>
            """
        )


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.html(
        """
        <div class="footer">

            YouTube RAG Intelligence System
            · FastAPI + Streamlit + Chroma
            + Ollama + Groq

        </div>
        """
    )


# ============================================================
# CHAT PAGE
# ============================================================

elif st.session_state.stage == "chat":


    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    header_col1, header_col2 = st.columns(
        [5, 1]
    )


    # ========================================================
    # HEADER LEFT
    # ========================================================

    with header_col1:

        st.html(
            f"""
            <div class="chat-header">

                <div>

                    <div class="chat-title">
                        🎥 YouTube AI Assistant
                    </div>

                    <div class="video-info">

                        Video ID:

                        <strong>
                            {st.session_state.video_id}
                        </strong>

                    </div>

                </div>


                <div class="chat-status">

                    <span class="status-dot"></span>

                    RAG Ready

                </div>

            </div>
            """
        )


    # ========================================================
    # NEW VIDEO BUTTON
    # ========================================================

    with header_col2:

        if st.button(
            "＋ New Video",
            use_container_width=True
        ):

            reset_app()

            st.rerun()


    # --------------------------------------------------------
    # EMPTY CHAT
    # --------------------------------------------------------

    if not st.session_state.messages:

        st.html(
            """
            <div class="empty-chat">

                <div class="empty-icon">
                    ✨
                </div>

                <div class="empty-title">
                    Your video is ready
                </div>

                <div class="empty-text">
                    Ask anything about the video.
                    Try asking about the main idea,
                    specific concepts, explanations,
                    comparisons, or important details.
                </div>

            </div>
            """
        )


    # --------------------------------------------------------
    # DISPLAY CHAT HISTORY
    # --------------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

    question = st.chat_input(
        "Ask something about this video..."
    )


    # --------------------------------------------------------
    # PROCESS QUESTION
    # --------------------------------------------------------

    if question:

        question = question.strip()


        if not question:

            st.stop()


        # ----------------------------------------------------
        # USER MESSAGE
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",

                "content": question
            }
        )


        with st.chat_message("user"):

            st.markdown(question)


        # ----------------------------------------------------
        # ASSISTANT
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


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.html(
        """
        <div class="footer">

            Powered by your RAG pipeline

        </div>
        """
    )