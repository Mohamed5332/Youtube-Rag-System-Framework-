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

    /* ============================================================
    GLOBAL
    ============================================================ */

    :root {
        --bg: #0f1117;
        --surface: #171a21;
        --surface-soft: #1c2029;
        --border: #2a2f3a;

        --text: #f1f3f5;
        --text-secondary: #a5acb8;
        --text-muted: #727b89;

        --accent: #ff4b4b;
        --accent-hover: #ff6262;

        --success: #35c46a;
    }


    .stApp {
        background:
            linear-gradient(
                180deg,
                #0f1117 0%,
                #11141b 55%,
                #0f1117 100%
            );

        color: var(--text);
    }


    /* ============================================================
    MAIN CONTAINER
    ============================================================ */

    .block-container {
        max-width: 1050px;

        padding-top: 3rem;
        padding-bottom: 3rem;
    }


    /* ============================================================
    HERO
    ============================================================ */

    .hero {
        text-align: center;

        padding-top: 65px;
        padding-bottom: 35px;
    }


    .hero-badge {
        display: inline-flex;
        align-items: center;

        padding: 6px 12px;

        border-radius: 6px;

        background: #1a1e27;
        border: 1px solid #2b313c;

        color: #b9c0cc;

        font-size: 12px;
        font-weight: 600;

        letter-spacing: 0.2px;

        margin-bottom: 22px;
    }


    .hero-title {
        font-size: 52px;

        font-weight: 750;

        letter-spacing: -1.8px;

        line-height: 1.05;

        color: #f5f6f8;

        margin-bottom: 18px;
    }


    .hero-subtitle {
        max-width: 650px;

        margin: 0 auto;

        color: var(--text-secondary);

        font-size: 16px;

        line-height: 1.7;
    }


    /* ============================================================
    URL CARD
    ============================================================ */

    .url-card {
        background: var(--surface);

        border: 1px solid var(--border);

        border-radius: 12px;

        padding: 24px;

        margin-top: 28px;

        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.18);
    }


    .input-label {
        color: #d8dce2;

        font-size: 13px;

        font-weight: 600;

        margin-bottom: 9px;
    }


    /* ============================================================
    TEXT INPUT
    ============================================================ */

    div[data-baseweb="input"] {
        background: #12151b;

        border-radius: 8px;

        border: 1px solid #303641;

        transition:
            border-color 0.18s ease,
            box-shadow 0.18s ease;
    }


    div[data-baseweb="input"]:hover {
        border-color: #414957;
    }


    div[data-baseweb="input"]:focus-within {
        border-color: #626b7a;

        box-shadow:
            0 0 0 1px rgba(255, 255, 255, 0.04);
    }


    /* ============================================================
    BUTTONS
    ============================================================ */

    .stButton > button {
        height: 46px;

        border-radius: 8px;

        border: 1px solid #ff4b4b;

        background: var(--accent);

        color: white;

        font-size: 14px;

        font-weight: 650;

        transition:
            background 0.18s ease,
            border-color 0.18s ease,
            transform 0.18s ease;
    }


    .stButton > button:hover {
        background: var(--accent-hover);

        border-color: var(--accent-hover);

        transform: translateY(-1px);
    }


    .stButton > button:active {
        transform: translateY(0);
    }


    /* ============================================================
    FEATURE CARDS
    ============================================================ */

    .feature-card {
        height: 100%;

        background: var(--surface);

        border: 1px solid var(--border);

        border-radius: 12px;

        padding: 22px;

        min-height: 165px;

        transition:
            border-color 0.2s ease,
            background 0.2s ease;
    }


    .feature-card:hover {
        background: #191d25;

        border-color: #3a414d;
    }


    .feature-icon {
        font-size: 24px;

        margin-bottom: 14px;
    }


    .feature-title {
        font-size: 15px;

        font-weight: 650;

        color: #e9ecf0;

        margin-bottom: 8px;
    }


    .feature-text {
        font-size: 13px;

        color: var(--text-secondary);

        line-height: 1.65;
    }


    /* ============================================================
    LOADING
    ============================================================ */

    .loading-container {
        text-align: center;

        padding-top: 90px;

        padding-bottom: 40px;
    }


    .loader {
        width: 42px;
        height: 42px;

        margin: auto;

        border-radius: 50%;

        border: 3px solid #292e38;

        border-top-color: #ff4b4b;

        animation:
            spin 0.85s linear infinite;
    }


    @keyframes spin {

        to {
            transform: rotate(360deg);
        }

    }


    .loading-title {
        font-size: 22px;

        font-weight: 650;

        color: #f1f3f5;

        margin-top: 20px;
    }


    .loading-text {
        color: var(--text-secondary);

        font-size: 13px;

        margin-top: 8px;

        line-height: 1.6;
    }


    /* ============================================================
    CHAT HEADER
    ============================================================ */

    .chat-header {
        display: flex;

        align-items: center;

        justify-content: space-between;

        padding: 16px 19px;

        margin-bottom: 20px;

        border-radius: 10px;

        background: var(--surface);

        border: 1px solid var(--border);
    }


    .chat-title {
        font-size: 19px;

        font-weight: 650;

        color: #f0f2f5;
    }


    .chat-status {
        font-size: 12px;

        color: #7ed99c;

        display: flex;

        align-items: center;

        gap: 7px;
    }


    .status-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: var(--success);
    }


    .video-info {
        display: inline-block;

        padding: 6px 9px;

        border-radius: 6px;

        background: #12151b;

        border: 1px solid #292f38;

        color: var(--text-muted);

        font-size: 11px;

        margin-top: 7px;
    }


    /* ============================================================
    EMPTY CHAT
    ============================================================ */

    .empty-chat {
        text-align: center;

        padding-top: 95px;

        padding-bottom: 80px;
    }


    .empty-icon {
        font-size: 44px;

        margin-bottom: 14px;
    }


    .empty-title {
        font-size: 22px;

        font-weight: 650;

        color: #eef0f3;

        margin-bottom: 9px;
    }


    .empty-text {
        color: var(--text-secondary);

        font-size: 14px;

        max-width: 530px;

        margin: auto;

        line-height: 1.7;
    }


    /* ============================================================
    STREAMLIT CHAT
    ============================================================ */

    /* User message */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: #181c23;

        border-radius: 10px;

        border: 1px solid #282e38;

        padding: 4px 12px;
    }


    /* Assistant message */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background: #13161c;

        border-radius: 10px;

        border: 1px solid #222832;

        padding: 4px 12px;
    }


    /* Chat input */

    [data-testid="stChatInput"] {
        background: #15181f;

        border-radius: 10px;

        border: 1px solid #303641;
    }


    [data-testid="stChatInput"]:focus-within {
        border-color: #4a5260;

        box-shadow:
            0 0 0 1px rgba(255, 255, 255, 0.03);
    }


    /* ============================================================
    ALERTS
    ============================================================ */

    [data-testid="stAlert"] {
        border-radius: 8px;

        border: 1px solid #303641;
    }


    /* ============================================================
    PROGRESS BAR
    ============================================================ */

    [data-testid="stProgressBar"] > div > div {
        background-color: #ff4b4b;
    }


    /* ============================================================
    FOOTER
    ============================================================ */

    .footer {
        text-align: center;

        color: #626b78;

        font-size: 11px;

        padding-top: 32px;

        padding-bottom: 8px;

        letter-spacing: 0.1px;
    }


    /* ============================================================
    RESPONSIVE
    ============================================================ */

    @media (max-width: 768px) {

        .block-container {
            padding-top: 1.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }


        .hero {
            padding-top: 35px;
        }


        .hero-title {
            font-size: 38px;

            letter-spacing: -1.2px;
        }


        .hero-subtitle {
            font-size: 14px;
        }


        .url-card {
            padding: 18px;
        }


        .chat-header {
            padding: 14px;
        }


        .chat-status {
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