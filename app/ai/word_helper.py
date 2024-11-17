from app.ai.anthropic_calls import AnthropicCalls
from anthropic import Anthropic
from flask import jsonify
import logging
import re
from app.config import ANTHROPIC_API_KEY, logger


def word_helper(word):
    try:
        # Initialize the client - you'll need to set ANTHROPIC_API_KEY in your environment
        client = Anthropic()
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

        q_and_a = AnthropicCalls(
            api_key=ANTHROPIC_API_KEY, 
            max_tokens=1024,
            system_prompt="You are a caring assistant tasked with helping an adult who's trying to learn how to read by providing context and examples for a given word.",
        )

        response = q_and_a.chat(
        f"Query: {message}\n\nThe user would like help to understand this word: {word}",
        should_print=False,
        clear_after_response=False
    )
        # Return just the text response
        # return message
        return response
        
    except Exception as e:
        return f"Error: {str(e)}"

def get_word_help(data):
    logger.isEnabledFor(logging.DEBUG)
    logger.debug("Word Helper API called")

    print(data)
    logger.debug(f"Data: {data}")
    word = data.get('word')
    if not word:
        return jsonify({'data': data}), 400
    logger.debug(f"Word Helper API called with word: {word}")
    response = word_helper(word)
    logger.debug(f"Word Helper API response: {response}")
    if type(response) == str:
        text_content = response
    else:
        text_content = response.content[0].text or response
    description_match = re.search(r'<description>(.*?)</description>', text_content, re.DOTALL)
    example_sentence_match = re.search(r'<example_sentence>(.*?)</example_sentence>', text_content, re.DOTALL)
    similar_sounds_match = re.search(r'<similar_sounds>(.*?)</similar_sounds>', text_content, re.DOTALL)
    description_text = description_match.group(1).strip()
    example_text = example_sentence_match.group(1).strip()
    similar_text = similar_sounds_match.group(1).strip()
    response_data = {
        "description": description_text,
        "example_sentence": example_text,
        "similar_sounds": similar_text
    }
    return jsonify(response_data)