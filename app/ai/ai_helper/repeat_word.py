from app.ai.anthropic_calls import AnthropicCalls
from app.config import ANTHROPIC_API_KEY

def repeat_word(word):
    try:
        # Initialize the client - you'll need to set ANTHROPIC_API_KEY in your environment
        USER_INPUT = [{'role': "user", 'message': f"the word is {word}"}]
        message = f"""
You are assisting with a program designed to help adults who are learning to read. Your task is to provide a brief explanation, usage example, and pronunciation guide for words that learners may not understand. This information should be clear, concise, and appropriate for adult learners.

The word to be explained is:
<word>
{word}
</word>

Please provide the following information for this word:

1. A brief description (1-2 sentences) that explains the meaning of the word in simple terms.

2. Use the word in a fairly simple sentence that is appropriate for adult learners. The sentence should provide context for the word's usage without being overly complex.

3. List 3-4 words that sound phonetically similar to help with pronunciation. These words should be common and easily recognizable.

Present your response in the following format:

<word_info>
<description>
[Insert brief description here]
</description>

<example_sentence>
[Insert example sentence here]
</example_sentence>

<similar_sounds>
[Insert phonetically similar words here, separated by commas]
</similar_sounds>
</word_info>

Ensure that all information is appropriate for adult learners and avoids overly childish or simplistic language while still being clear and easy to understand."""

        ai_help = AnthropicCalls(
            api_key=ANTHROPIC_API_KEY, 
            max_tokens=1024,
            system_prompt="You are a caring assistant tasked with helping an adult who's trying to learn how to read by providing context and examples for a given word.",
        )

        response = ai_help.chat(
        f"Query: {message}\n\nThe user would like help to understand this word: {word}",
        should_print=False,
        clear_after_response=False
    )

        return response
        
    except Exception as e:
        return f"Error: {str(e)}"