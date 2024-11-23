from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

#automatically looks for an "ANTHROPIC_API_KEY" environment variable
client = Anthropic()

def eval_repeat_words(data, chat):
    try:
        EXERCISE_DATA = data['exercise_details']
        # USER_REQUEST = data['user_request']
        prompt = f"""
You are an AI assistant evaluating an adult learner's literacy exercise. Your task is to analyze the learner's responses, identify any words they may have struggled with, and offer additional practice if needed.

You will be provided with a JSON object containing the exercise data. Here is the exercise data:

<exercise_data>
{EXERCISE_DATA}
</exercise_data>

Inside the <exercise_data> you will find the questions asked with the mistakes made by the user.

You also have a record of the chat so far:
<chat>
{chat}
</chat>

Follow these steps to complete the evaluation:`

1. Parse the JSON object to extract the exercise description and the list of user responses.

2. For each question in the exercise:
   a. Identify the words the user was asked to repeat.
   b. Check whether the user made any mistakes.
   c. Summarize their performance being kind and encouraging whilst keeping the summary brief.

3. If the user made any mistakes, offer to provide additional practice, if they got all words in 1 try, don't offer additional exercises:
   a. Ask if they would like to practice a few more similar words.

4. Only if the user has made mistakes:
    a. Provide 6 words that use the same phonics as the mistakes.
    b. Format your response in the following way: <evaluation>[Include your summary here]</evaluation><add_words>[Include the additional words here]</add_words>
    c. Ignore the rest of the instructions, 4.c. is your response.

5. Format your response as follows (Do not include any newlines):

<evaluation>[Include your summary here]</evaluation>

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