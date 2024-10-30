import os
import json

import pandas as pd
import numpy as np

from dotenv import load_dotenv
# from sqlite_calls import SQLiteCalls
from anthropic_calls import AnthropicCalls
from anthropic import Anthropic
from sklearn.metrics.pairwise import cosine_similarity
from flask import jsonify


load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

LLM_calls = AnthropicCalls(api_key=ANTHROPIC_API_KEY, stream=True)


def ai_answer_question(question, CHAT_HISTORY):
    print('\n::\n CHAT HISTORY: ', CHAT_HISTORY, '\n\n::')
    try:
        # Initialize the client - you'll need to set ANTHROPIC_API_KEY in your environment
        client = Anthropic()
        USER_INPUT = [{'role': "user", 'message': question}]
        message = f"""
Here is the chat history so far:

<chat_history>
{CHAT_HISTORY}
</chat_history>

You are an AI assistant designed to assess the reading ability of adult learners (ages 20-30) who have enrolled in a literacy program. Your goal is to determine their reading level, which may range from no ability to middle school level. Approach this task with respect and sensitivity, as you are interacting with adults who are working to improve their literacy skills.

And here is the user's latest input:

<user_input>
{USER_INPUT}
</user_input>

Guidelines for the assessment:

1. Focus on assessing the user's current reading ability, not teaching them to read.
2. Ask one question at a time and wait for an answer.
3. Keep your questions or responses to 25 words or less, unless absolutely necessary.
4. Use language that is appropriate for the learner's perceived level, avoiding words like "simple" or "complex."
5. Do not repeat questions that have already been asked in the chat history.
6. Remember that the user's input is being converted from speech to text, so they cannot control capitalization or punctuation.
7. When asking the user to read a word or sentence, place it at the end of your response after a colon. This ensures the speech synthesizer doesn't read it aloud. End the sentenvce with a full stop.
8. Avoid asking to repeat or spell short words (e.g., cat, car, fun, pot). Instead, ask the user to use such words in a sentence.
9. The user's vocal response is being converted into text by a simple (and not extremely accurate) speech recognition program, if a user appears to get something wrong, ask a similar (but not identical) question before considering it incorrect.
10. DONT REPEAT THE INSTRUCTIONS FROM THE FIRST QUESTION ON EVERY SUSEQUENT QUESTION

Assessment Process:
1. Ask questions to gauge the user's reading ability. Focus on:
   - Vocabulary understanding
   - Sentence reading
   - Concept comprehension
2. Analyze responses, considering:
   - Vocabulary use
   - Sentence complexity
   - Comprehension level
   - Overall communication ability
3. Continue asking questions until you have sufficient information to make an assessment (aim for no more than 10 questions).
4. Provide a reading age evaluation when you have gathered enough information.

Before each response, wrap your analysis in <analysis> tags. In this analysis:
1. Summarize the user's response and note any key observations.
2. Evaluate the user's current estimated reading level based on their responses so far.
3. Identify areas that need further assessment.
4. Plan your next question or evaluation, considering the guidelines and avoiding short words.

When providing a reading age evaluation, briefly explain your assessment and provide an estimated reading age.

Format your response as follows:

<response>
Your response to the user, following the guidelines above.
</response>
<continue>
true or false (indicating whether the conversation should continue)
</continue>

Example output structure (generic, without specific content):

<analysis>
[Thorough analysis of user's response, current estimated reading level, areas needing assessment, and plan for next question or evaluation]
</analysis>

<response>
[Question or evaluation based on the analysis, following the guidelines]
</response>
<continue>
[true/false value]
</continue>"""

        q_and_a = AnthropicCalls(
            api_key=ANTHROPIC_API_KEY, 
            max_tokens=1024,
            system_prompt="You are a caring assistant tasked with helping to assess the reading ability of adult learners. You will ask questions to determine their reading level, which may range from no ability to middle school level. You will provide an estimated reading age based on their responses. You will also follow the guidelines provided in the prompt. You will provide your responses in the format specified in the prompt.",
        )

        response = q_and_a.chat(
        f"Query: {message}\n\nSaves generated questions in JSON format.",
        should_print=False,
        clear_after_response=False
    )
        # Return just the text response
        # return message
        return response
        
    except Exception as e:
        return f"Error: {str(e)}"

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
        f"Query: {message}\n\nSaves generated questions in JSON format.",
        should_print=False,
        clear_after_response=False
    )
        # Return just the text response
        # return message
        return response
        
    except Exception as e:
        return f"Error: {str(e)}"














generate_questions_call = AnthropicCalls(
    api_key=ANTHROPIC_API_KEY, 
    max_tokens=1024,
    system_prompt="You are a helpful assistant that is helping the user to paractice for an interview. You will generate 2 questions to help them practice their interview skills. If the user has very little experience, please focus on questions that will explore how they will tackle scenarios that are new to them but also relevant to the position. Don't mention exactly how many years of experience they have as these are rouugh figures (especially if the user has 10 years experience). YOU MUST USE THE TOOL PROVIDED FOR YOUR REPLIES\n"
)

def generated_questions(query: str):
    generator_tool = {
        "name": "save_interview_questions",
        "description": "Provides interview questions in JSON format when the user asks for interview questions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "question1": {
                    "type": "string",
                    "description": "Interview question"
                },
                "question2": {
                    "type": "string",
                    "description": "Interview question"
                },
                "question3": {
                    "type": "string",
                    "description": "Interview question"
                },
                "question4": {
                    "type": "string",
                    "description": "Interview question"
                },
                "question5": {
                    "type": "string",
                    "description": "Interview question"
                }
            },
            "required": ["question"]
        },     
    }
    
    response = generate_questions_call.chat(
        f"Query: {query}\n\nSaves generated questions in JSON format.",
        should_print=False,
        tools = [generator_tool],
        clear_after_response=False
    )
    questions = []
    print('\n\n',response)


    # if response.stop_reason == "tool_use":
    for item in response.content:
        # print(item)
        if item.type == "tool_use":
            questions.append({'question_text': item.input["question1"], 'is_generated': True})
            questions.append({'question_text': item.input["question2"], 'is_generated': True})

        #     for question in item.input:
        #         obj = {"question_text": question["question"]}

            # if item.type == "tool_use":
            #     if item.name == "save_interview_questions":
            #         print("\nTool_use: ", item)
            #         print("------")
            #         return item.input.get("chunk", False)
    # questions_json = json.dumps(questions)
    return questions


def generate_questions_claude(user_questions, data):
    experience = data.get('experience')
    job_title = data.get('job_title')
    job_str = f"The user is applying for a position as a {job_title}" if job_title else ""
    exp_str = f"The user has {experience} years of experience" if experience else ""
    user_questions_list = user_questions.to_dict(orient='records')
    u_qs = [question["question_text"] for question in user_questions_list]
    message = f"Please generate 2 job interview questions for the user. {job_str} {exp_str}. The user already has some questions to work from so please make your suggestions not too similar to theirs. Their saved questions are: {u_qs}. IT IS IMPORTANT THAT YOU USE THE TOOL PROVIDED! "

    new_questions = generated_questions(message)
    print('\n\n',new_questions,'\n\n')
    if isinstance(new_questions, str):
        new_questions = json.loads(new_questions)
    # print ('\n\n',new_questions,'\n\n')
    return new_questions


# def get_context(embedding, role="", n=1):
#     chat_df = SQL_calls.load_chat_to_dataframe(role)
#     context = find_top_n_similar(chat_df, embedding, n)
#     return context


# def find_top_n_similar(df, user_input_embedding, n=5):
#     if df.empty or 'embedding' not in df.columns:
#         print("The DataFrame is empty or missing the 'embedding' column.")
#         return pd.DataFrame()
    
#     df['embedding'] = df['embedding'].apply(
#         lambda emb: json.loads(emb) if isinstance(emb, str) else emb
#     )
#     df['similarity'] = df['embedding'].apply(
#         lambda emb: similarty_search(user_input_embedding, emb)
#     )

#     top_n_df = df.sort_values(by='similarity', ascending=False).head(n)
#     # To have messages in the correct order
#     top_n_df = top_n_df.sort_values(by='date', ascending=True)

#     return top_n_df


# def similarty_search(embedding1, embedding2):
#     embedding1 = np.array(embedding1).reshape(1, -1)
#     embedding2 = np.array(embedding2).reshape(1, -1)

#     similarity = cosine_similarity(embedding1, embedding2)

#     return similarity[0][0]

# def is_relevant(chunk: str, query: str):
#     response = context_determinator.chat(
#         f"Query: {query}\n\nChunk: {chunk}\n\nIs this chunk relevant to the query? Respond in JSON format.",
#         should_print=False,
#         clear_after_response=True
#     )
#     print("Chunk:\n", chunk)
#     print("Response:\n", response.content[0].text)
#     return json.loads(response.content[0].text)["is_relevant"]

# if __name__ == "__main__":
#     load_dotenv()
#     ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

#     LLM_calls = AnthropicCalls(api_key=ANTHROPIC_API_KEY, stream=True)
#     SQL_calls = SQLiteCalls("key_words.db")
#     context_determinator = AnthropicCalls(
#         api_key=ANTHROPIC_API_KEY, 
#         max_tokens=400,
#         system_prompt="You are a helpful assistant that determines if a chunk of text is relevant to a given query.\n" +
#             "Respond with JSON object containing a boolean 'is_relevant' field and a 'reason' field explaining your decision"
#     )

#     user_data_extractor = AnthropicCalls(
#         api_key=ANTHROPIC_API_KEY, 
#         max_tokens=1024,
#         system_prompt="You are a helpful assistant that extracts chunk of user related data from given query.\n"
#     )

#     conversation()
