import pandas as pd
from config import TABLE


df = pd.read_csv(TABLE)

new_df = df['Страна']

countries = []

for country in new_df:
    if country not in countries:
        countries.append(country)

