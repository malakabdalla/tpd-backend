from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

#automatically looks for an "ANTHROPIC_API_KEY" environment variable
client = Anthropic()

def evaluate_repeat_words_exercise(data, chat):
    try:
        EXERCISE_DATA = data['exercise_data']
        QUESTIONS = data['questions']
        USER_INTERACTIONS = data['User interactions']
        # USER_REQUEST = data['user_request']
        prompt = f"""
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

You also have a record of the chat so far:
<chat>
{chat}
</chat>

Follow these steps to complete the evaluation:

1. Parse the JSON object to extract the exercise description and the list of user responses.

2. For each question in the exercise:
   a. Identify the words the user was asked to repeat.
   b. Check the number of times the user engaged with each word.
   c. If a user engaged with a word more than once, consider it a word they may have struggled with.
   d. Summarize their performance being kind and encouraging whilst keeping the summary brief.

3. If the user struggled with any words, offer to provide additional practice, if they got all words in 1 try, don't offer additional exercises:
   a. Ask if they would like to practice a few more similar words.
   b. Don't mention that they had difficulty with the words, rather say that you notice that they practiced them more than others.

4. If you have offered to practice similar words and the user agrees:
    a. Provide 7 words that use the same phonics as the struggled words.
    b. Format your response in the following way: <prompt>[Include prompt here - less than 8 words]</prompt><add_words>[Include the additional words here]</add_words>
    c. Ignore the rest of the instructions and provide the additional exercise.

5. Format your response as follows (DO NOT INCLUDE ANY NEWLINES OR ADDITIONAL TEXT):

<evaluation><summary>[Include your summary here]</summary></evaluation>

Remember to be encouraging and supportive in your feedback, as the goal is to help the adult learner improve their literacy skills.
"""

        response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {'role': 'user', 'content': prompt}
        ]
    )

        return response.content[0].text
        
    except Exception as e:
        return f"Error: {str(e)}"