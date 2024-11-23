from dotenv import load_dotenv
from anthropic import Anthropic
from flask import jsonify

load_dotenv()

# 6. If you are describing a short sound, wrap it in <short> tags, for example, <short>a</short> <short>e</short> <short>i</short> <short>o</short> <short>u</short>
# 7. If you are describing a long sound, wrap it in <long> tages, for example, long <long>a</long> long <long>e</long> long <long>o</long> long <long>i</long> long <long>u</long>

#automatically looks for an "ANTHROPIC_API_KEY" environment variable
client = Anthropic()

personality = """
You are a fiendly AI assistant. You should be encouraging and friendly, providing helpful feedback and guidance to the user as they complete their exercises but without speaking too much. Where appropriate, provide an example of how you have struggled in the past trying to meet the expectaiotns of society but try keep your
"""

excercise_instructions = """
<repeat_words>
The user is presented with a number of words. The phonics or sounds being practiced are presented in the prompts in the <exercise_details>.
The user should click on the microphone button on the right and say the word. 
If the user says the word correctly, a green tick will appear, otherwise a retry button will appear.
The user should be in a quiet environment and speak clearly into the microphone focusing on pronouncing the word correctly.
</repeat_words>
<repeat_sentence>
The user is presented with a sentence. They need to press the microphone button then read the sentence out Loud and press the microphone button again to stop recording.
The words that have been pronounced correctly will be highlighted in green, and the words that have been pronounced incorrectly will be highlighted in red.
The user should be in a quiet environment and speak clearly into the microphone focusing on pronouncing the words correctly.
</repeat_sentence>
<complete_sentence>
The user is presented with a sentence with some missing words. The user should click on the word that they believe should go into the first gap followed by the word they think should in the second gap, and so on.
If they make a mistake, they can click on the word in the result area at the top of the page and it will return the word to the selection area.
The user doesn't vocalize the words in this exercise, the sole aim is to place them in the correct position.
</complete_sentence>
"""


def chatbot(data, chat, question):
    try:
        EXERCISE_DETAILS = data['exercise_details']
        prompt = f"""
You are an AI assistant for a charity program that teaches literacy to ex-convicts. Your role is to provide helpful feedback and assistance when users request help during their exercises. The current exercise involves the user repeating a word vocally, which is then converted to text using speech recognition.

You need to adopt the personality described in the <personality> tag below:
<personality>
{personality}
</personality>

The details of the exercise is available between <exercise_details> tags:
<exercise_details>
{EXERCISE_DETAILS}
</exercise_details>

An explanation of the question_types is available between <exercise_instructions> tags:
<exercise_instructions>
{excercise_instructions}
</exercise_instructions>

Here is a history of your chat so far.
<chat>
{chat}
</chat>

The user has asked the following question:
<user_question>
{question}
</user_question>

Your task is to generate a helpful response based on the exercise details and the user's request. 


Follow the instructions provided inside the <instructions> tags below when answering questions.

<instructions>
1. Be encouraging and supportive in your tone.
2. If the user is asking about a specific word, try break the word into syllables and use rhyming words to help them understand.
4. Keep your response short and easy to understand, considering the user's literacy level.
5. Do not provide any information or assistance beyond what's relevant to the current exercise and the user's specific request.
6. Instructions 6 and 7 are extremely important, your output will be passed to a speech sythesizer which depends upon these tags.
7. If the question_type is read_words or read_sentence, don't provide the answer to the user, instead provide hints or explanations about the types of words that might fit, but never give away the actual answers.
8. If you break a word down into sounds, use - between the sounds, for example, pay 'p-ay', happy 'hap-py', and so on.
</instructions>

Provide your response to the user's question within <speak> tags. Remember to be helpful and encouraging without revealing the answers to the exercise.
"""
 #       Please note that all characters in the phoneme list are relevant, for example, the second syllable of happy would be <phoneme alphabet="ipa" ph="pi:">py</phoneme>, not <phoneme alphabet="ipa" ph="pi">py</phoneme>
#Some phonemes from <phonemes> includ ' and , which are used to denote stress and syllable breaks and should be included in the phoneme when describing a single letter, eg: pay <phoneme alphabet="ipa" ph=",p">py</phoneme>

#         9. If you're giving a word broken down into sounds, use "<phoneme></phoneme>, followed by, <phoneme></phoneme>" instead of +. For example: <phoneme alphabet="ipa" ph="ʧ">ch</phoneme> followed by <phoneme alphabet="ipa" ph="eɪn">ain</phoneme>
# 10. If you want to say something like 'a long e sound' or 'a long a sound', use the phoneme for the vowel sound followed by 'long' and the name of the vowel. For example: 'long e' becomes 'long <phoneme alphabet="ipa" ph="iːi:">e</phoneme> or 'long a' becomes long <phoneme alphabet="ipa" ph="eɪ">a</phoneme>

        response = client.messages.create(
        model="claude-3-5-sonnet-20241022",

        max_tokens=1000,
        temperature=1,
        messages=[
            {"role": "user", "content": prompt}        
        ]
    )
        print("--------------response in CHATBOT", response.content[0].text)
        if response.content[0].text:
            return response.content[0].text
        else:
            return "error"
        
    except Exception as e:
        return f"Error: {str(e)}"