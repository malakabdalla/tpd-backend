from dotenv import load_dotenv
from anthropic import Anthropic
from flask import jsonify

load_dotenv()

#automatically looks for an "ANTHROPIC_API_KEY" environment variable
client = Anthropic()

def repeat_words(data, chat, question):
    try:
        EXERCISE_DETAILS = data['exercise_details']
        prompt = f"""
You are an AI assistant for a charity program that teaches literacy to ex-convicts. Your role is to provide helpful feedback and assistance when users request help during their exercises. The current exercise involves the user repeating a word vocally, which is then converted to text using speech recognition.

Here are the details of the current exercise:
<exercise_details>
{EXERCISE_DETAILS}
</exercise_details>

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
2. If the user is asking about a specific word, provide a clear and simple explanation.
3. If appropriate, suggest words that sound similar to help with pronunciation or understanding.
4. Offer tips on how to approach the exercise if the user seems confused.
5. Keep your response short and easy to understand, considering the user's literacy level.
6. Do not provide any information or assistance beyond what's relevant to the current exercise and the user's specific request.
7. The user is presented with the words in 'data' and must select them one at a time and records themselves saying the word.
8. Do not use quotes for examples, rather use commas before and after each example or sound
9. Every time you refer to a sound using letters, wrap them in pipes, for example, |a|, |b|, |c|, |e|, |i|, |o|, |u|, long |a|, long |e|, long |i|, long |o|, long |u|

Formulate your response as a string that can be printed and synthesized into audio feedback.The response should be clear, helpful, and directly address the user's request while taking into account the exercise details.
</instructions>

Present your response within <speak> tags within <answer> tags. Do not include any other text or explanations outside of these tags.
"""
        
 #       Please note that all characters in the phoneme list are relevant, for example, the second syllable of happy would be <phoneme alphabet="ipa" ph="pi:">py</phoneme>, not <phoneme alphabet="ipa" ph="pi">py</phoneme>
#Some phonemes from <phonemes> includ ' and , which are used to denote stress and syllable breaks and should be included in the phoneme when describing a single letter, eg: pay <phoneme alphabet="ipa" ph=",p">py</phoneme>

#         9. If you're giving a word broken down into sounds, use "<phoneme></phoneme>, followed by, <phoneme></phoneme>" instead of +. For example: <phoneme alphabet="ipa" ph="ʧ">ch</phoneme> followed by <phoneme alphabet="ipa" ph="eɪn">ain</phoneme>
# 10. If you want to say something like 'a long e sound' or 'a long a sound', use the phoneme for the vowel sound followed by 'long' and the name of the vowel. For example: 'long e' becomes 'long <phoneme alphabet="ipa" ph="iːi:">e</phoneme> or 'long a' becomes long <phoneme alphabet="ipa" ph="eɪ">a</phoneme>

        response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}        
        ]
    )
        print("--------------response in eval repeat words", response.content[0].text)
        if response.content[0].text:
            return response.content[0].text
        else:
            return "error"
        
    except Exception as e:
        return f"Error: {str(e)}"