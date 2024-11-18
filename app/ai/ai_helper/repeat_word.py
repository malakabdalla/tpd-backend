from app.ai.anthropic_calls import AnthropicCalls
from app.config import ANTHROPIC_API_KEY

def repeat_word(data):
    try:
        EXERCISE_DETAILS = data['exercise_details']
        USER_REQUEST = data['user_request']
        # Initialize the client - you'll need to set ANTHROPIC_API_KEY in your environment
        message = f"""
You are an AI assistant for a charity program that teaches literacy to ex-convicts. Your role is to provide helpful feedback and assistance when users request help during their exercises. The current exercise involves the user repeating a word vocally, which is then converted to text using speech recognition.

You will be given two pieces of information:

1. Exercise details:
<exercise_details>
{EXERCISE_DETAILS}
</exercise_details>

This object contains the exercise description and other relevant details about the current task.

2. User's request for help:
<user_request>
{USER_REQUEST}
</user_request>

This is the specific help or clarification the user is seeking.

Your task is to generate a helpful response based on the exercise details and the user's request. Consider the following guidelines when crafting your response:

1. Be encouraging and supportive in your tone.
2. If the user is asking about a specific word, provide a clear and simple explanation.
3. If appropriate, suggest words that sound similar to help with pronunciation or understanding.
4. Offer tips on how to approach the exercise if the user seems confused.
5. Keep your response concise and easy to understand, considering the user's literacy level.
6. Do not provide any information or assistance beyond what's relevant to the current exercise and the user's specific request.

Formulate your response as a string that can be printed and synthesized into audio feedback. The response should be clear, helpful, and directly address the user's request while taking into account the exercise details.

Present your response within <answer> tags. Do not include any other text or explanations outside of these tags."""

        ai_help = AnthropicCalls(
            api_key=ANTHROPIC_API_KEY, 
            max_tokens=1024,
            system_prompt="The user has a query about this exercise which involves repeating words vocally.",
        )

        response = ai_help.chat(
        f"Query: {message}",
        should_print=False,
        clear_after_response=False
    )

        return response
        
    except Exception as e:
        return f"Error: {str(e)}"