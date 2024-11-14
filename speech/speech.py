from google.cloud import texttospeech

def synthesize_speech_with_specific_voice(text):
    # Initialize the Text-to-Speech client
    client = texttospeech.TextToSpeechClient()

    # Set the text input
    input_text = texttospeech.SynthesisInput(text=text)

    # Specify the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB",
        name="en-GB-Wavenet-A",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Configure audio output
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Call the API to synthesize speech
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # Return the audio content as binary data
    return response.audio_content