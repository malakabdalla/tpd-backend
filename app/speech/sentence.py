from google.cloud.speech_v2 import SpeechClient
from google.api_core.client_options import ClientOptions
from google.cloud.speech_v2.types import cloud_speech
from app.config import PROJECT_ID, logger

def get_sentence(audio_content: bytes, phrase: str) -> cloud_speech.RecognizeResponse:
    """Enhances speech recognition accuracy using an inline phrase set.
    Args:
        audio_content (bytes): The audio content in bytes
        phrase (str): The phrase to boost recognition for
    Returns:
        cloud_speech.RecognizeResponse: The full response object which includes the transcription results.
    """
    # Instantiates a client
    # client = SpeechClient({'api_endpoint': 'europe-west4-speech.googleapis.com'})
    client_options_var = ClientOptions(
    api_endpoint="europe-west4-speech.googleapis.com"
    )
    client = SpeechClient(client_options=client_options_var)
    # Build inline phrase set to produce a more accurate transcript
    phrase_set = cloud_speech.PhraseSet(
        phrases=[{"value": phrase, "boost": 5}]
    )
    adaptation = cloud_speech.SpeechAdaptation(
        phrase_sets=[
            cloud_speech.SpeechAdaptation.AdaptationPhraseSet(
                inline_phrase_set=phrase_set
            )
        ]
    )
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        adaptation=adaptation,
        # language_codes=["en-GB"],
        # model="long",
        features=cloud_speech.RecognitionFeatures(
            enable_word_confidence=True,
        ),
    )

    # Prepare the request
    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/europe-west4/recognizers/tpd",
        config=config,
        content=audio_content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        logger.debug(f"Transcript: {result.alternatives[0].transcript}")
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response