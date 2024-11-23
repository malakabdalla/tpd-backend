from typing import Dict
from dotenv import load_dotenv
import os
from anthropic import Anthropic
import json

class Game2Configuration:
    def __init__(self):
        # Instance attributes (can vary per game)
        self.system_prompt = """You are an educational expert in UK specialising in phonics and reading comprehension.
        Your task is to generate a short text and questions to the text. 
        Goal is to test an adult learner's English reading and comprehension skills
        The questions should help assess and improve their understanding of the text.
        """
        self.model = "claude-3-5-sonnet-20241022"
        self.response_format = """
        {
            "title": "[text's title]",
            "text": "[text]",
            "text_topic": "[chosen text topic]",
            "focus_words": ["[word1]", "[word2]", "[word3]"],
            "questions": [
                {
                "question_id": "[1]",
                "question_type": "[type]",
                "question_text": "[text]",
                "options": {
                    "a": "[option1]",
                    "b": "[option2]",
                    "c": "[option3]",
                    "d": "[option4]"
                },
                "correct_answer": "[a]",
                "hint": "[hint text]",
                "explaination": "[explaination text]"
            }
        ]
        }"""
        self.example = """
        {
            "title": "A Tennis Champion's Journey",
            "text": "Katy knew she had to work harder to become a tennis champion. Over the years, her love for the sport grew stronger. She trained daily until she achieved her dreams.",
            "text_topic": "sport",
            "focus_words": ["knew", "work", "love"],
            "questions": [
                {
                "question_id": "1",
                "question_type": "Basic comprehension",
                "question_text": "What sport is the text about?",
                "options": {
                    "a": "Football",
                    "b": "Tennis",
                    "c": "Basketball",
                    "d": "Swimming"
                },
                "correct_answer": "b",
                "hint": "Look for specific mentions of sports in the text.",
                "explanation": "The text clearly states that Katy wanted to become a tennis champion, making tennis the central sport discussed."
                }
            ]
            }"""

class ComprehensionGenerator:
    def __init__(self):
        load_dotenv()
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.config = Game2Configuration()
        self.q_number = 3
        self.focus_words_nbr = 3
        self.words_in_text = 40
    
        self.q_types = """
        - Basic comprehension
        - Vocabulary understanding
        - Main idea identification
        """
                    
    def build_prompt(self, focus_words: str, topic:str) -> str:
        return f"""
            STEP 1:
            Please generate the interesing text for reading with topic about {topic}. Text must be suitable for target group. 20-30 words in the text.
            Use exactly {self.focus_words_nbr} words from this list:
            <focus words>
            {focus_words}
            </focus words>

            STEP 2:
            Generate questions for this text based on the following guidelines:
            Number of questions: {self.q_number}.
            Randomly choose the type of questions from this list {self.q_types}\
            Provide:
            - title
            - text
            - The question
            - Type
            - Multiple choice options (4 choices)
            - The correct answer
            - Hint, 10-20 words in the hint text
            - Explanation why this answer is correct, around {self.words_in_text} words in Explanation text
            - list of sight words used in the text
            Return response in this exact JSON structure:
            <JSON structure>
            {self.config.response_format}
            </JSON structure>

            EXAMPLE OF ONE QUESTION:
            <example>
            {self.config.example}
            </example>

            QUALITY CHECKS:
            - Verify natural flow of text
            - Check the response, only JSON file.
            """

    def generate_text_and_questions(self, focus_words: str, topic:str) -> Dict:
        try:
            prompt = self.build_prompt(focus_words, topic)
            print(prompt)
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=4000,
                system=self.config.system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.content[0].text
            # result_json = json.loads(result)
            return result
        except Exception as e:
            return f"Error in generate_exercises: {str(e)}"

def GameComprehension(hard_words):
    try:
        hard_words_level3 = ["so", "work", "love", "their", "one", "over", "sure", "two", "knew", "because", "only", "woman", "done", "does", "other"]
        hard_words_phonics_3 = ["burn", "hurt", "church", "blur", "curl", "fur", "furnish", "Thursday", "turn", "slur", "surf", "burst"]

        focus_words = hard_words
        topic = "sport"

        generator = ComprehensionGenerator()

        # # Generate exercises
        result = generator.generate_text_and_questions(focus_words, topic)
        result_json = json.loads(result)
        result_json["questions"][0]["question_type"] = "basic_comprehension"
        result_json["questions"][1]["question_type"] = "basic_comprehension"
        return result_json
    except Exception as e:
        return f"Error: {str(e)}"
    



