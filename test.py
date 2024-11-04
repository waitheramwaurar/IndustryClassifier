# Example of how to use the industry classifier module :)

import IndustryClassifier as ic
import pandas as pd
# import os
# import time

data = pd.read_csv("All Companies.csv", encoding='unicode_escape')

data = data[1800:]

companies_list = ic.get_companies(data)

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

model = ic.configure_model('GEMINI_API_KEY_1')

company_industry_map = ic.classify_companies(companies_list, categories, model)

# Map the results to the dataframe
data["Company Industry"] = data["Company Name"].map(company_industry_map)

# print(data)

# Save the results to a new CSV
data.to_csv('CompaniesWithIndustriesEighteenthBatch.csv', index=False)
