"""OpenAI API connector."""

# Import from standard library
import os
import logging

# Import from 3rd party libraries
import openai
from openai import OpenAI


api_key = "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"

# Assign credentials from environment variable or streamlit secrets dict
client = OpenAI(
    # This is the default and can be omitted
    api_key=api_key,
)


class Openai:
    """OpenAI Connector."""

    @staticmethod
    def moderate(prompt: str) -> bool:
        """Call OpenAI GPT Moderation with text prompt.
        Args:
            prompt: text prompt
        Return: boolean if flagged
        """
        try:
            response = client.moderations.create(input=prompt)
            return response.results[0].flagged

        except Exception as e:
            logging.error(f"OpenAI API error: {e}")

    @staticmethod
    def complete(prompt: str) -> str:
        """Call OpenAI GPT Completion with text prompt.
        Args:
            prompt: text prompt
        Return: predicted response text
        """
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt},
                ],
                model="gpt-3.5-turbo"
            )
            return response.choices[0].message.content

        except Exception as e:
            logging.error(f"OpenAI API error: {e}")

    @staticmethod
    def image(prompt: str) -> str:
        """Call OpenAI Image Create with text prompt.
        Args:
            prompt: text prompt
        Return: image url
        """
        try:
            response = client.images.generate(
                prompt=prompt,
                n=1,
                size="512x512",
                response_format="url",
            )
            return response.data[0].url

        except Exception as e:
            logging.error(f"OpenAI API error: {e}")