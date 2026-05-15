from openai import OpenAI

from case_analysis.config.settings import (
    OPENAI_API_KEY
)



class OpenAIService:

    def __init__(self):

        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

    def analyze_case(self, case):

        prompt = f"""
        Analyze this Salesforce support case.

        Subject:
        {case['Subject']}

        Status:
        {case['Status']}
        """

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content