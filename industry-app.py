import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import RequestOptions
from google.api_core import retry

# Load environment variables
load_dotenv()

# Configure Gemini API with API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# List of industry categories
categories = [
    'Academic', 'Agriculture', 'Asset Management', 'Automotive', 'Aviation', 'Bakery', 'Banking', 'Biotechnology',
    'Building Material', 'Business Association', 'Business Process Outsourcing (BPO)', 'Chemicals', 
    'Coffee processing and Export', 'Cold storage warehousing', 'Construction', 'Construction Material',
    'Consulting', 'Co-operative Organisation', 'Diplomacy', 'Education', 'Electrical contractor', 'Electronics',
    'Energy', 'Engineering', 'Entertainment', 'Environmental', 'Equity Investors', 'Fast Moving Consumer Goods (FMCG)',
    'Food & Beverage', 'General trade', 'Government', 'Healthcare', 'Heavy Machinery', 'Home & Office Furnishings',
    'Hospitality & Leisure', 'Hygiene and sanitation', 'Insurance', 'Internet and Telecommunication',
    'Investment advisory', 'Legal', 'Logistics', 'Logistics & Warehousing', 'Manufacturing', 'Marketing & Communications',
    'Media', 'Medical Equipment', 'Metals & Mining', 'Mining', 'NGO', 'Oil & Gas', 'Other', 'Packaging',
    'Pharmaceuticals Products', 'Plastics & Rubber', 'Port Services', 'Production of Alcoholic Beverages',
    'Production of Gas Cylinders', 'Production of Steel', 'Pulp & Paper', 'Real Estate Developer', 
    'Recruitment services', 'Religious Institution', 'Retail', 'Security & Defence', 'Software Engineering', 'Solar',
    'Technology', 'Telecommunications', 'Textile & Clothing', 'Textiles & Apparel', 'Tours and Travel', 
    'Town planning', 'Transportation', 'Utilities', 'Warehousing', 'Water Solutions'
]

# Load company data from CSV
data = pd.read_csv('CompaniesTest.csv')
companies_list = data['Company Name'].to_list()

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Base prompt template
base_prompt = f"Please look through this list of industries: {categories} and tell me what industry this company fits into. If you cannot find the company, give the industry as 'NA'."

# Function to create a prompt for each company
def create_prompt(company):
    """
    Creates a customized prompt for each company.
    """
    return base_prompt + f" Give your answer in the format of 'Company: Industry'. Do not put anything in bold and don't put additional info, thank you. The company in question is {company}."

# Function to convert the model's string response into a dictionary
def str_to_dict(response_string):
    """
    Convert the string response from the model into a dictionary.
    Assumes the format is 'Company: Industry'.
    """
    try:
        company, industry = response_string.strip().split(': ', 1)
        return {company: industry}
    except ValueError:
        return {}  # Return an empty dictionary if the response format is incorrect

# Main function to fetch industry classification
def classify_companies(companies_list):
    """
    For each company in the list, classify its industry using the Gemini model.
    Returns a dictionary with company names as keys and their industries as values.
    """
    master_dict = {}
    
    for company in companies_list:
        prompt = create_prompt(company)
        try:
            response = model.generate_content(
                prompt, 
                request_options=RequestOptions(retry=retry.Retry(initial=10, multiplier=2, maximum=60, timeout=300))
            )
            res_string = response.text
            master_dict.update(str_to_dict(res_string))
        except Exception as e:
            print(f"Error classifying {company}: {e}")
            master_dict[company] = 'NA'
    
    return master_dict

# Fetch the classifications
company_industry_map = classify_companies(companies_list)

# Map the results to the dataframe
data["Company Industry"] = data["Company Name"].map(company_industry_map)

# Print the updated dataframe
print(data)
