#%%
import pandas as pd 

url = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv'

df = pd.read_csv(url)
# %%
df.head()
# %%
df.columns
# %%
#df.groupby('class')['survived'].apply(lambda x : x.sum()/x.count())
#df.groupby('class')['survived'].apply(lambda x : x.mean())
df.groupby('class')['survived'].mean()
# %%
df['who'].value_counts()
# %%
df['sex'].value_counts()
# %%
df['adult'] = df['age'] >= 18

df.loc[df['adult']==True, 'adult']  = 'Adult'
df.loc[df['adult']==False, 'adult'] = 'Child'
# %%
df.groupby(['class', 'adult', 'sex'])['survived'].mean()
# %%
prob_not_surv_ad_male = 1 - df.loc[df['adult_male'], 'survived'].mean()
# %%
df.loc[df['adult_male']].groupby('class')['survived'].apply(lambda x : 1-x.mean())
# %%
