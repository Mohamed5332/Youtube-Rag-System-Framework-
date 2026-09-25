
from langchain_community.document_loaders import YoutubeLoader
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.documents import Document
from urllib.parse import urlparse, parse_qs

def load_documents(youtube_url):

    languages = [
        "en",
        "ar"
    ]

    for language in languages:

        try:

            print(
                f"Trying transcript language: {language}"
            )

            loader = YoutubeLoader.from_youtube_url(
                youtube_url=youtube_url,
                language=language
            )

            documents = loader.load()

            if documents:

                print(
                    f"Transcript loaded using: {language}"
                )

                return documents

        except Exception as e:

            print(
                f"Could not load {language}: {e}"
            )

    raise RuntimeError(
        "Could not find an English or Arabic transcript "
        "for this YouTube video."
    )



def extract_video_id(youtube_url):

    parsed_url = urlparse(youtube_url)

    if "youtu.be" in parsed_url.netloc:
        return parsed_url.path.strip("/")

    return parse_qs(parsed_url.query)["v"][0]


def load_documents_v2(youtube_url):

    video_id = extract_video_id(youtube_url)

    print("=" * 70)
    print("VIDEO ID:", video_id)

    api = YouTubeTranscriptApi()

    transcript_list = api.list(video_id)

    print("AVAILABLE TRANSCRIPTS:")

    for transcript in transcript_list:
        print(
            "language:",
            transcript.language_code,
            "|",
            transcript.language,
            "| generated:",
            transcript.is_generated
        )

    # --------------------------------------------------
    # Prefer Arabic or English original transcript
    # --------------------------------------------------

    selected_transcript = None

    for language in ["en", "ar"]:

        try:

            selected_transcript = transcript_list.find_transcript(
                [language]
            )

            print(
                "SELECTED TRANSCRIPT:",
                selected_transcript.language_code
            )

            break

        except Exception:

            continue

    if selected_transcript is None:

        raise RuntimeError(
            "No English or Arabic transcript was found."
        )

    # --------------------------------------------------
    # Fetch transcript
    # --------------------------------------------------

    transcript_data = selected_transcript.fetch()

    text = " ".join(
        item.text
        for item in transcript_data
    )

    print("TRANSCRIPT LENGTH:", len(text))

    # --------------------------------------------------
    # Convert to LangChain Document
    # --------------------------------------------------

    document = Document(
        page_content=text,
        metadata={
            "video_id": video_id,
            "language": selected_transcript.language_code,
            "is_generated": selected_transcript.is_generated
        }
    )

    return [document]