import pandas as pd

# Using the csv files that have been returned by the IndustryClassifier module, split the three categories into three different dataframes (and/or csv) 
# Create empty dataframes for the three categories: 
# The missing entries, the ones the LLM could not categorise and the ones that have been succefully categorised

empty_df = pd.DataFrame()
notfound_df = pd.DataFrame()
classified_df = pd.DataFrame()

files = ['CompaniesWithIndustriesFirstBatch.csv','CompaniesWithIndustriesSecondBatch.csv','CompaniesWithIndustriesThirdBatch.csv','CompaniesWithIndustriesFourthBatch.csv','CompaniesWithIndustriesFifthBatch.csv','CompaniesWithIndustriesSixthBatch.csv',
         'CompaniesWithIndustriesSeventhBatch.csv', 'CompaniesWithIndustriesEighthBatch.csv', 'CompaniesWithIndustriesNinthBatch.csv', 'CompaniesWithIndustriesTenthBatch.csv', 'CompaniesWithIndustriesEleventhBatch.csv', 'CompaniesWithIndustriesTwelvethBatch.csv']


for file in files:
    file_path = file

    df = pd.read_csv(file_path, encoding='unicode_escape')

    # Split data based on the conditions in column
    df_blank = df[df['Company Industry'].isna()]
    df_blank['Company Industry'] = df_blank['Company Industry'].fillna("MISSING")
    df_nf = df[df['Company Industry'] == "Not Found"]
    df_other = df[(df['Company Industry'].notna()) & (df['Company Industry'] != 'Not Found')]

    empty_df = pd.concat([empty_df, df_blank], ignore_index=True)
    notfound_df = pd.concat([notfound_df, df_nf], ignore_index=True)
    classified_df = pd.concat([classified_df, df_other], ignore_index=True)

# empty_df.to_csv("Missing_Companies.csv")
# notfound_df.to_csv("Not_Categorised.csv")
# classified_df.to_csv("Classified_Companies.csv")

print(classified_df.head(50))

