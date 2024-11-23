# from dataclasses import dataclass
from typing import Dict
from dotenv import load_dotenv
import os
from anthropic import Anthropic
import json

class GameConfiguration:
    def __init__(self):
        # Instance attributes (can vary per game)
        self.target_group = "adults (20-50 years old) struggling with reading and having basic vocabulary and comprehension abilities"
        self.model = "claude-3-5-sonnet-20241022"
        self.system_prompt = """You are an educational expert specializing in UK phonics and reading instruction for adult learners. """
        self.response_format = """
        {
        "questions": [
            {
            "question_id": "[1]",
            "question_type": "complete_sentence",
            "context": "[context category]",
            "phonics": "[sound pattern]",
            "patterns": "[spelling pattern]",
            "question_text": ["sentence with %//gap//%"],
            "gaps": [number of gaps],
            "options": ["option", "option"],
            "correct_order": ["option", "option"]
            }
        ]
        }
        """

        self.example = """
        {
          "questions": [
            {
            "question_id": "1",
            "question_type": "complete_sentence",
            "context": "Daily Activities",
            "phonics": "long 'a' sound",
            "patterns": "a_e, ai",
            "question_text": ["Every morning, I %//gap//% breakfast at eight. The %//gap//% was falling as I walked to work."],
            "gaps": 2,
            "options": ["rain", "make"],
            "correct_order": ["make", "rain"]
            }
        ]
        }"""


class GapFillGenerator:
    """Class to handle gap fill exercise generation"""
    def __init__(self):
        load_dotenv()
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.config = GameConfiguration()
        self.sent_nbr = 2
        self.gaps_nbr = 3
        
    def build_prompt(self, focus_phonics: str) -> str:
        return f"""
        Your task is to create engaging gap-fill sentences focusing on specific phonics patterns.
        Please carefully read the following information and instructions before proceeding.        
        <focus phonics>
        {focus_phonics}
        </focus pohonics>
        
        TARGET AUDIENCE: 
        - {self.config.target_group}
        EDICATIONAL GOALS:
        - Reinforce phonics patterns
        - Develop contextual understanding
        
        INSTRUCTIONS:
        1. Generate this number of sentences {self.sent_nbr}, each containing {self.gaps_nbr} gaps (indicated by %//missing word//%)
        2. Each sentence must:
            - be clear and practical
            - include sufficient context clues for comprehension
            - contain 15-30 words
            - be grammatically correct and natural-sounding
        3. Focus on the specified phonics patterns, ensuring that the gaps correspond to words exemplifying these patterns.
        4. Present options in random order
        5. If using multiple phonics patterns, list all patterns used
        6. Return response in this exact JSON structure:
        <JSON structure>
        {self.config.response_format}
        </JSON structure>

        EXAMPLE OF ONE QUESTION:
        <example>
        {self.config.example}
        </example>

        QUALITY CHECKS:
        - Ensure readability at basic level
        - Verify natural flow of text
        - Confirm appropriate context clues
        - Check the response, only JSON file.
        """
    def generate_exercises(self, focus_phonics: str) -> Dict:
        try:
            prompt = self.build_prompt(focus_phonics)
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

def frontend_transform_json(input_json):
    try:
        new_json = {
            "questions": []
        }    
        for question in input_json["questions"]:
            new_question = {
                "question_id": question["question_id"],
                "question_type": question["question_type"],
                "prompts": question["question_text"],
                "gaps": question["gaps"],
                "data": question["options"],
                "answers": question["correct_order"]
            }
            new_json["questions"].append(new_question)
        return new_json
    except Exception as e:
        return f"Error in frontend_transform_json: {str(e)}"

def GameFillGap():
    try:
        patterns = [
            {
                'sound': 'er',
                'pattern': 'er',
                'examples': ["her", "term", "bitter", "herb", "infer", "better", "chatter", "verb", "faster", "transfer", "stern"]
            },
            {
                'sound': 'er',
                'pattern': 'ur',
                'examples': ["burn", "hurt", "church", "blur", "curl", "fur", "furnish", "Thursday", "turn", "slur", "surf", "burst"]
            },
            {
                'sound': 'er',
                'pattern': 'ir',
                'examples': ["first", "dirt", "skirt", "sir", "bird", "girl", "birthday", "thirty", "stir", "third", "firm", "birth"]
            },
            {
                "sound": "(Long) ō",
                "pattern": "o_e",
                "examples": ["hope", "smoke", "note", "slope", "rode", "code", "cope", "home", "mope", "spoke", "bone", "cone", "dome", "hole", "joke", "lone", "mode", "nose", "pole", "role", "rope", "rose", "tone", "vote", "woke", "zone", "broke", "choke", "close", "drove", "froze", "globe", "phone", "quote", "stone", "those", "whole", "wrote", "probe", "scope"]
            },
        ]

        # Create the full focus_phonics
        focus_phonics = "Please do proper analysis of phonics and focus on these phonics patterns:\n"
        for pattern in patterns:
            focus_phonics += f"""
            - the '{pattern['sound']}' sound in the form of the '{pattern['pattern']}' patterns (letter combinations), "examples": {pattern['examples']}"""
        
        # Initialize the generator
        generator = GapFillGenerator()

        # # Generate exercises
        result = generator.generate_exercises(focus_phonics)
        # print(result)

        result_json = json.loads(result)
        # print(f"json {result_json}/n/n")

        result_frontend_json = frontend_transform_json(result_json)

        # with open('game3_questions.json', 'w') as json_file:
        #     json.dump(result_frontend_json, json_file, indent=4)
        print(result_frontend_json)
        
        return result_frontend_json
    except Exception as e:
        return f"Error: {str(e)}"
    