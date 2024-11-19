from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

#automatically looks for an "ANTHROPIC_API_KEY" environment variable
client = Anthropic()

def evaluate_repeat_words_exercise(data):
    try:
        EXERCISE_DATA = data['exercise_data']
        QUESTIONS = data['questions']
        USER_INTERACTIONS = data['User interactions']
        # USER_REQUEST = data['user_request']
        message = f"""
You are an AI assistant evaluating an adult learner's literacy exercise. Your task is to analyze the learner's responses, identify any words they may have struggled with, and offer additional practice if needed.

You will be provided with a JSON object containing the exercise data. Here is the exercise data:

<exercise_data>
{EXERCISE_DATA}
</exercise_data>

You will also receive a list of questions and the user's interactions with each word. Here are the questions and user interactions:
<questions>
{QUESTIONS}
</questions>

<user_interactions>
{USER_INTERACTIONS}
</user_interactions>

Follow these steps to complete the evaluation:

1. Parse the JSON object to extract the exercise description and the list of user responses.

2. For each question in the exercise:
   a. Identify the words the user was asked to repeat.
   b. Check the number of times the user engaged with each word.
   c. If a user engaged with a word more than once, consider it a word they may have struggled with.

3. Create a list of words the user may have struggled with.

4. Prepare a brief summary of the user's performance, including:
   a. The total number of questions in the exercise.
   b. The number of words the user may have struggled with.
   c. A list of these words, if any.

5. If the user struggled with any words, offer to provide additional practice, if they got all words in 1 try or less, don't offer additional exercises:
   a. Ask if they would like to practice a few more similar words.
   b. If yes, provide 3-5 words that use the same phonics as the struggled words.
   c. Don't mention that they had difficulty with the words, rather say that you notice that they practiced them more than others.

6. Format your response as follows (DO NOT INCLUDE ANY NEWLINES OR ADDITIONAL TEXT):

<evaluation><summary>[Include your summary here]</summary><struggled_words>[List the words the user struggled with, if any]</struggled_words><additional_practice>[If applicable, include your offer for additional practice with additional 7 comma separated words between the add_words tags]</additional_practice><add_words>[Include the additional words here]</add_words></evaluation>

Remember to be encouraging and supportive in your feedback, as the goal is to help the adult learner improve their literacy skills.
"""

        response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": """
             'exercise_name': 'Reading long vowel sounds',
             'data' : ['week', ' speak', ' happy', 'keen', 'sorry', 'cheat', 'tree'],
             'Description': "
             Remember that vowel sounds can be long or short. The 
             long vowel sounds are ā, ē, ō, ĩ and ũ', "the short ones are a, e, i, o, 
             and u. In this activity you'll be reading words containing long vowel 
             sounds. There are seven words for each long vowel sound and all the letter 
             combinations you've learnt so far for each sound will feature here. Read each 
             word as it appears on the screen"},
             'questions': [{'Question Number': 0, 'Question Type': 'repeat_words', 'Prompts': ['ai, ay'], 'Data': ['day', 'main', 'rain', 'say', 'hay', 'mail', 'rail'] }],
             'User interactions': {'day': 3, 'main': 1, 'rain': 1, 'say': 1, 'hay': 4, 'mail': 1, 'rail': 1},
            'sight_words': "so work love their one over sure two knew because only woman done does other", 
            'user_request': 'Why have you grouped all of these words together?'""",
            "role": "assistant", "content": """
            <evaluation><summary>Overall, the user showed good comprehension with most words, 
             requiring only one attempt</summary><struggled_words>day, hay</struggled_words>
             <additional_practice>You seem to have practised some words several times.
             Would you like to practice some more with similar words? These words all 
             use the same 'ay' pattern and long 'a' sound as in \"pay\". Would you like to 
             practice these words together? Remember: The 'ay' pattern usually comes at 
             the end of words and makes the long 'a' sound, just like in \"pay\".
             </additional_practice><add_words>day,way,say,play,stay</add_words></evaluation>"
            """,
            "role": "user", "content": """
             'exercise_name': 'Reading long vowel sounds',
             'data' : ['week', ' speak', ' happy', 'keen', 'sorry', 'cheat', 'tree'],
             'Description': "
             Remember that vowel sounds can be long or short. The 
             long vowel sounds are ā, ē, ō, ĩ and ũ', "the short ones are a, e, i, o, 
             and u. In this activity you'll be reading words containing long vowel 
             sounds. There are seven words for each long vowel sound and all the letter 
             combinations you've learnt so far for each sound will feature here. Read each 
             word as it appears on the screen"},
             'questions': [{'Question Number': 0, 'Question Type': 'repeat_words', 'Prompts': ['ai, ay'], 'Data': ['day', 'main', 'rain', 'say', 'hay', 'mail', 'rail'] }],
             'User interactions': {'lay': 1, 'stain': 1, 'rail': 1, 'may': 1, 'lay': 1, 'hail': 1, 'rail': 1},
            'sight_words': "so work love their one over sure two knew because only woman done does other", 
            'user_request': 'Why have you grouped all of these words together?'""",
            "role": "assistant", "content": """
            "<evaluation><summary>The exercise contained 7 words testing long vowel sounds. 
            The user successfully read all words on their first attempt. This shows good 
            comprehension of the 'ai' and 'ay' long vowel sound patterns.</summary>
            <struggled_words>None</struggled_words><additional_practice></additional_practice>
            <add_words></add_words></evaluation>""",
            "role": "user", "content": f"{message}"}
        ]

    )

        return response.content[0].text
        
    except Exception as e:
        return f"Error: {str(e)}"