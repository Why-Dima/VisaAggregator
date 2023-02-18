import pandas as pd


df = pd.read_csv('https://docs.google.com/spreadsheets/d/1yU5voi5LJzovBl8IhoXGRNF9lJlotArVPQiZRlO0e1U/export?format=csv')

new_df = df['Страна']

countries = []

for country in new_df:
    if country not in countries:
        countries.append(country)

# # data = df[df. == 'Виза типа "C"'][['Цель поездки']]
# # print(data)
# # dfs = df, index=[new_df]
# dfs = df[lambda x: x['Страна'] == 'Австрия']
# # print(dfs)
# dfs = pd.DataFrame(dfs)
# dfss = dfs[dfs['Тип визы'] == 'Виза типа "C"']

