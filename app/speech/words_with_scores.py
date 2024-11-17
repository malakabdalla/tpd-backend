from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from app.config import PROJECT_ID

def transcribe_word_scores(
    audio_content: bytes
) -> cloud_speech.RecognizeResponse:
    """Transcribes a local audio file into text with word-level confidence.
    Args:
        audio_file (str): Path to the local audio file to be transcribed.
            Example: "resources/audio.wav"
    Returns:
        cloud_speech.RecognizeResponse: The response containing the
            transcription results with word-level confidence.
    """
    # Instantiates a client
    client = SpeechClient()

    # # Reads a file as bytes
    # with open(audio_file, "rb") as file:
    #     audio_content = file.read()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["en-GB"],
        model="long",
        features=cloud_speech.RecognitionFeatures(
            enable_word_confidence=True,
        ),
    )

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/global/recognizers/_",
        config=config,
        content=audio_content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response
