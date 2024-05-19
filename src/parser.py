import os
import json
from typing import Optional
import openai
from dotenv import load_dotenv
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback


class Receipt(BaseModel):
    """Information extracted by an OCR engine from a document."""

    receipt: bool = Field(
        default=False,
        description="Determines if the information retrieved corresponds to a receipt or not."
    )
    restaurant_meals: bool = Field(
        default=False,
        description="In case the document is a receipt, determines if it contains restaurant meals or not. If it doesn't contain restaurant meals, assign False."
    )
    number_of_people_in_invoice: Optional[int] = Field(
        default=None,
        description="According to the restaurant meals, determines how many people have eaten at the restaurant. Assume that each person eats regular portions. Try to group all items ordered to improve your estimate."
    )


def validate_openai_api_key():
    """Checks if openAI API key exists and if it is valid"""

    # Load the .env file and get the API key
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')

    # Return in case API key was not defined
    if not api_key:
        return {"ERROR": "API key not found.", "status": "error", "data": "",
        "message": "Please set the OPENAI_API_KEY environment variable."}, 422

    openai.api_key = api_key
    try:
        openai.models.list()
    except openai.AuthenticationError as e:
        return {"ERROR": "API key not valid.", "status": "error", "data": "",
        "message": e}, 422

    return True

def get_structured_output(ocr_content, model="gpt-3.5-turbo-0125"):
    """Obtain JSON output from LLM"""

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert extraction algorithm. "
                "Only extract relevant information from the text. "
                "If you do not know the value of an attribute asked to extract, "
                "return null for the attribute's value.",
            ),
            (   "human",
                "{text}"
            ),
        ]
    )

    # Use openAI model
    model = ChatOpenAI(model=model, temperature=0)

    # Append schema to prompt
    runnable = prompt | model.with_structured_output(schema=Receipt)

    # Output is the Receipt class with its attributes
    with get_openai_callback() as cb:
        output = runnable.invoke({"text": str(ocr_content)})
        print(f"API Cost ($): {round(cb.total_cost, 4)}")

    # Convert output to dictionary
    output_dict = output.__dict__

    # Convert dictionary to JSON format
    output_json = json.dumps(output_dict)

    return output_json
