import pandas as pd

nba_teams = {
    'Hawks': 1,
    'Lakers': 2,
    'Celtics': 3
}

df = pd.DataFrame.from_dict(nba_teams, orient='index')
df.columns = ['Rating']
df.index.name = 'Team'
print(df)