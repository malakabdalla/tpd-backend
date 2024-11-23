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

import html
import boto3
import os
from openai import OpenAI
import dotenv

dotenv.load_dotenv()
aws_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

def text_to_ssml(input) -> str:
    """
    Generates SSML text from plaintext.
    Given an input filename, this function converts the contents of the text
    file into a string of formatted SSML text. This function formats the SSML
    string so that, when synthesized, the synthetic audio will pause for two
    seconds between each line of the text file. This function also handles
    special text characters which might interfere with SSML commands.

    Args:
        inputfile: name of plaintext file
    Returns: SSML text based on plaintext input
    """

    # Parses lines of input file

    # Replace special characters with HTML Ampersand Character Codes
    # These Codes prevent the API from confusing text with
    # SSML commands
    # For example, '<' --> '&lt;' and '&' --> '&amp;'

    escaped_lines = html.escape(input)

    # Convert plaintext to SSML
    # Wait two seconds between each address
    ssml = "<speak>{}</speak>".format(
        escaped_lines.replace("\n", '\n<break time="2s"/>')
    )
    print("escaped :::::", ssml)
    # Return the concatenated string of ssml script
    return ssml

def make_phonemes(text):
    print("text here ::::::: ", text)
    text = text.replace('<sound>a</sound>', '<phoneme alphabet=\\"ipa\\" ph=\\"æeɪ\\"/>')
    text = text.replace('<sound>A</sound>', '<break time="100ms"/><phoneme alphabet="ipa" ph="æeɪ">A</phoneme>')

    text = text.replace('<sound>p</sound>', '<break time="200ms"/><phoneme alphabet=\\"ipa\\" ph=\\"pɛ\\">p</phoneme><break time="250ms"/>')
    text = text.replace('<sound>P</sound>', '<break time="200ms"/><phoneme alphabet="ipa" ph="pʰ">P</phoneme><break time="250ms"/>')

    # text = text.replace('A', '<phoneme alphabet="ipa" ph="`eɪ">a</phoneme>')
    print(text)
    return text

def synthesize_speech_with_specific_voice(text) -> None:


    # Instantiates a client
    # client = texttospeech.TextToSpeechClient()

    # ssml = text_to_ssml(text)
    # # Sets the text input to be synthesized
    
    # phonemes = make_phonemes(ssml)
    # print("ssml :::::: ", phonemes)
    # synthesis_input = texttospeech.SynthesisInput(ssml=phonemes)

    # # Builds the voice request, selects the language code ("en-US") and
    # # the SSML voice gender ("MALE")
    # voice = texttospeech.VoiceSelectionParams(
    #     language_code="en-GB",
    #     # name="en-GB-Wavenet-A",
    #     name="en-GB-Neural2-A",
    #     # name="en-GB-News-G",
    #     # name="en-GB-News-I",
    #     # name="en-GB-Journey-F", not working
    #     # name="en-GB-Studio-C",
    #     ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    # )

    # # Selects the type of audio file to return
    # audio_config = texttospeech.AudioConfig(
    #     audio_encoding=texttospeech.AudioEncoding.MP3
    # )

    # # Performs the text-to-speech request on the text input with the selected
    # # voice parameters and audio file type
    # response = client.synthesize_speech(
    #     input=synthesis_input, voice=voice, audio_config=audio_config
    # )

    # # # Writes the synthetic audio to the output file.
    # # with open("test_example.mp3", "wb") as out:
    # #     out.write(response.audio_content)
    # #     print("Audio content written to file " + "test_example.mp3")
    # return response.audio_content

    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("SECRET_ACCESS_KEY_ID")

    # Sets the text input to be synthesized
    client = OpenAI()
    response = client.audio.speech.create(
    model="tts-1",
    voice="fable",
    input=text,
)

    audio = response.read()
    return audio