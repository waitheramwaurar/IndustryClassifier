import pandas as pd
import numpy as np
import google.generativeai as genai
from google.generativeai.types import RequestOptions
from google.api_core import retry
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# 1. Create a list of industries or sectors that your companies might belong to.

categories = ['Academic', 'Agriculture', 'Asset Management', 'Automotive', 'Aviation', 'Bakery', 'Banking', 'Biotechnology', 'Building Material',
'Business Association', 'Business Process Outsourcing (BPO)', 'Chemicals', 'Coffee processing and Export', 'Cold storage warehousing', 'Construction', 'Construction Material',
'Consulting', 'Co-operative Organisation', 'Diplomacy', 'Education', 'Electrical contractor', 'Electronics', 'Energy', 'Engineering', 'Entertainment', 'Environmental',
'Equity Investors', 'Fast Moving Consumer Goods (FMCG)', 'Food & Beverage', 'General trade', 'Government', 'Healthcare', 'Heavy Machinery', 'Home & Office Furnishings',
'Hospitality & Leisure', 'Hygiene and sanitation', 'Insurance', 'Internet and Telecommunication', 'Investment advisory', 'Legal', 'Logistics', 'Logistics & Warehousing',
'Manufacturing', 'Marketing & Communications', 'Media', 'Medical Equipment', 'Metals & Mining', 'Mining', 'NGO', 'Oil & Gas', 'Other', 'Packaging', 'Pharmaceuticals Products',
'Plastics & Rubber', 'Port Services', 'Production of Alcoholic Beverages', 'Production of Gas Cylinders', 'Production of Steel', 'Pulp & Paper', 'Real Estate Developer',
'Recruitment services', 'Religious Institution', 'Retail', 'Security & Defence', 'Software Engineering', 'Solar', 'Technology', 'Telecommunications', 'Textile & Clothing',
'Textiles & Apparel', 'Tours and Travel', 'Town planning', 'Transportation', 'Utilities', 'Warehousing', 'Water Solutions']

# 2. Store the company names in a list or read them from a file or database
data =  pd.read_csv('CompaniesTest.csv')

companies_list = data['Company Name'].to_list()

# Create new column and add data depending on the company

# print(data.head())

# 3. Select a Web Scraping/Search Method OR Use LLM - Gemini AI

# Create a base prompt
base_prompt = f"Please look through this list of different industries: {categories} and tell me what industry this company fits into. If you cannot find the company, give industry as 'NA'"

model = genai.GenerativeModel("gemini-1.5-flash")

# Convert model into a key-value pair

def str_to_dict(response_string):
    """
    Parameter: response_string
    The function takes the response from the model, which is in string format and converts it into key-value pair (dictionary) form
    Returns: res_dict
    The function returns the passed string as a key value pair without any trailing spaces or new-line characters
    """
    res_list = response_string.rstrip().split(': ')

    # print(res_list[1])

    res_dict = {res_list[0]:res_list[1]}

    return res_dict

# List that will store the key-value pairs from the model
dict_list = []

for company in companies_list:

    prompt = base_prompt + f"Give your answer in the format of 'Company: Industry', do not put anything in bold and don't put additional info, thank you. The company in question is {company}"
    # Set up delay between consecutive requests
    response = model.generate_content(prompt, request_options=RequestOptions(retry=retry.Retry(initial=10, multiplier=2, maximum=60, timeout=300))) 
    # print(response.text)
    res_string = response.text
    dict_list.append(str_to_dict(res_string))


master_dict = {} 

for item in dict_list:
    master_dict.update(item)

# print(master_dict)

# 4. Match the Company to an Industry
data["Company Industry"] = data["Company Name"].map(master_dict)

print(data)

# ----> Testing Part <------

# prompt = base_prompt + f"Give your answer in the format of 'Company: Industry', do not put anything in bold and don't put additional info, thank you. The company in question is U.S. Depratment of Commerce International Trade Administration"
# response = model.generate_content(prompt, request_options=RequestOptions(retry=retry.Retry(initial=10, multiplier=2, maximum=60, timeout=300))) 
# print(response.text)

# res_string = response.text
# print(str_to_dict(res_string))

# print(type(str_to_dict(res_string)))

# 5. Store the Results - covert updated df to csv

# 6. Handle Rate Limits & Errors
