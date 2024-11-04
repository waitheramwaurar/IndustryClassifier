# This is more modular code

import os
# import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import RequestOptions
from google.api_core import retry

# Load the LLM API
def configure_model(api_key):
    """
    Load API key of LLM from environment variables
    """
    load_dotenv()
    genai.configure(api_key=os.environ[api_key])
    return genai.GenerativeModel("gemini-1.5-flash")

# Get the data
def get_companies(data):
    """
    Load the raw data that will be used
    """
    companies_list = data['Company Name'].to_list()

    return companies_list

# Initialize model
def create_prompt(company, categories):
    """
    Initializes the LLM model and returns the base prompt
    """
    base_prompt = f"Please look through this list of industries: {categories} and tell me what industry this company fits into. If you cannot find the company, give the industry as 'Not Found'."
    
    return base_prompt + f" Give your answer in the format of 'Company:Industry'. Do not put anything in bold and don't put additional info, thank you. The company in question is {company}."

# Function to convert the model's string response into a dictionary
def str_to_dict(response_string):
    """
    Convert the string response from the model into a dictionary.
    Assumes the format is 'Company:Industry'.
    """
    try:
        company, industry = response_string.strip().split(':', 1)
        return {company: industry}
    except ValueError:
        return {}  # Return an empty dictionary if the response format is incorrect

# Main function to fetch industry classification
def classify_companies(companies_list,categories,model):
    """
    For each company in the list, classify its industry using the Gemini model.
    Returns a dictionary with company names as keys and their industries as values.
    """
    master_dict = {}
    
    for company in companies_list:
        prompt = create_prompt(company,categories)
        try:
            response = model.generate_content(
                prompt, 
                request_options=RequestOptions(retry=retry.Retry(initial=10, multiplier=2, maximum=60, timeout=200))
            )
            res_string = response.text
            master_dict.update(str_to_dict(res_string))
        except Exception as e:
            print(f"Error classifying {company}:{e}")
            master_dict[company] = 'Not Found'
    
    return master_dict    
