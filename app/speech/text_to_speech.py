from google.cloud import texttospeech

# def synthesize_speech_with_specific_voice(text):
#     # Initialize the Text-to-Speech client
#     client = texttospeech.TextToSpeechClient()

#     # Set the text input
#     input_text = texttospeech.SynthesisInput(text=text)

#     # Specify the voice parameters
#     voice = texttospeech.VoiceSelectionParams(
#         language_code="en-GB",
#         name="en-GB-Wavenet-A",
#         ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
#     )

#     # Configure audio output
#     audio_config = texttospeech.AudioConfig(
#         audio_encoding=texttospeech.AudioEncoding.MP3
#     )

#     # Call the API to synthesize speech
#     response = client.synthesize_speech(
#         input=input_text, voice=voice, audio_config=audio_config
#     )

#     # Return the audio content as binary data
#     return response.audio_content

def synthesize_speech_with_specific_voice(ssml_text) -> None:
    """
    Generates SSML text from plaintext.
    Given a string of SSML text and an output file name, this function
    calls the Text-to-Speech API. The API returns a synthetic audio
    version of the text, formatted according to the SSML commands. This
    function saves the synthetic audio to the designated output file.

    Args:
        ssml_text: string of SSML text
    """

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Sets the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Builds the voice request, selects the language code ("en-US") and
    # the SSML voice gender ("MALE")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB",
        # name="en-GB-Wavenet-A",
        # name="en-GB-Neural2-A",
        # name="en-GB-News-G",
        name="en-GB-News-I",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Selects the type of audio file to return
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Performs the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # # Writes the synthetic audio to the output file.
    # with open("test_example.mp3", "wb") as out:
    #     out.write(response.audio_content)
    #     print("Audio content written to file " + "test_example.mp3")
    return response.audio_content