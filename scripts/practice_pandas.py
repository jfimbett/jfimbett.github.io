#%%
import pandas as pd
import numpy as np

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

df = pd.read_csv(url)

print(df.head())
# %%
# describe variables
print(df.describe())

#%%
# what % of passengers survived?
n_s = len(df[df.Survived==1])
n   = len(df)
print(f"Percentage of passengers that survived: {n_s/n*100:.2f}%")
# %%
# passangers per class
print(df['Pclass'].value_counts())

# Rename the classes 
df['Pclass'] = df['Pclass'].replace([1,2,3],['first','second','third'])
print(df['Pclass'].value_counts())
# %%
# By class what is the minimum, maximum, median and average age?
print(df.groupby('Pclass')['Age'].agg(['min','max','median','mean']))
# %%
# What is the name and age of the oldest survivor?
print(df[df['Survived']==1][['Name','Age']].sort_values('Age',ascending=False).head(1))
# %%
# What is the name and age of the youngest survivor?
print(df[df['Survived']==1][['Name','Age']].sort_values('Age',ascending=True).head(1))

# %%
# What % of men did not survive?
for s in ["male", "female"]:
    n_s = len(df[(df.Sex==s) & (df.Survived==0)])
    n   = len(df[df.Sex==s])
    print(f"Percentage of {s} that did not survive: {n_s/n*100:.2f}%")

# %%
# What % of children did not survive?
n_s = len(df[(df.Age<18) & (df.Survived==0)])
n   = len(df[df.Age<18])
print(f"Percentage of children that did not survive: {n_s/n*100:.2f}%")

# %%
# % of survivors by class
for c in ["first", "second", "third"]:
    n_s = len(df[(df.Pclass==c) & (df.Survived==1)])
    n   = len(df[df.Pclass==c])
    print(f"Percentage of {c} class that survived: {n_s/n*100:.2f}%")
# %%
df["Last Name"] = df.Name.str.split(",").str[0]
# most common last names?
print(df["Last Name"].value_counts().head(5))
# %%
# embarked - Port of Embarkation (C = Cherbourg; Q = Queenstown; S = Southampton)
print(df["Embarked"].value_counts())

# % of survivors by port of embarkation
for e in ["C", "Q", "S"]:
    n_s = len(df[(df.Embarked==e) & (df.Survived==1)])
    n   = len(df[df.Embarked==e])
    print(f"Percentage of {e} port that survived: {n_s/n*100:.2f}%")
# %%
# What explains that more than half of passengers from Cherbourg survived?
# In what class they travelled?
print(df[df.Embarked=="C"]["Pclass"].value_counts())
# %%
# Gender of passengers from Cherbourg
print(df[df.Embarked=="C"]["Sex"].value_counts())
# %%
# What % of female in first clas survived?

for e in df.Embarked.dropna().unique():
    mask = (
        (df.Embarked==e) & 
        (df.Pclass=="first") & 
        (df.Sex == "female")
        )

    n_s = len(df[mask & (df.Survived==1)])
    n   = len(df[mask])

    print(f"Embarked {e}: {n_s/n*100:.2f}%")
# %%
# What did the average survivor paid, compared to the average non-survivor?
print(df.groupby('Survived')['Fare'].mean())
# %%
# SibSp - # of siblings / spouses aboard the Titanic
# Where people with family more likely to survive?
for s in sorted(df.SibSp.unique()):
    n_s = len(df[(df.SibSp==s) & (df.Survived==1)])
    n   = len(df[df.SibSp==s])
    print(f"Percentage of people with {s} siblings/spouses that survived: {n_s/n*100:.2f}%")
# %%
# Exercise in class:
# What is the ex-ante average person most likely to survive?
# E.g. Compute the probability of survival 
# conditioning on all possible combinations of the categorical variables

def most_likely_survivor(df):
    pass