#%%
import pandas as pd 
from matplotlib import pyplot as plt

df = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv')
# %%

# 1. 
# Probability of survival for a passenger in each class
survival_prob = df.groupby('class')['survived'].mean()

# 2.
# Probability of survival for a passenger
survival_prob = df.groupby(['class', 'who'])['survived'].mean()

# 3.

# compute P(not surviving and male) and P(not surviving and male | class)
not_surviving_male = 1- df[df['who'] =='man']['survived'].mean()
# for each class 
for c in df['class'].unique():
    prob_not_surviving = 1 - df[(df['who'] == 'male') & (df['class'] == c)]['survived'].mean()

    # diff 
    if abs(not_surviving_male - prob_not_surviving) < 0.01:
        print(f"Events independent for class {c}") 


# Estimate the average age of the passengers who survived and the passengers who did not survive.

avg_age = df.groupby('survived')['age'].mean()

# Estimate the average fare paid by the passengers who survived and the passengers who did not survive.

avg_fare = df.groupby('survived')['fare'].mean()

# Based on the documentation of pandas and matplotlib, create a plot that shows the relatiin between the fare paid and the age of the passengers.



plt.scatter(df['age'], df['fare'])
plt.xlabel('Age')
plt.ylabel('Fare')
plt.title('Fare vs Age')
plt.show()

#%%
# now witht different colors for the different classes
colors = {'First': 'red', 'Second': 'blue', 'Third': 'green'}

# empty figure 
fig, ax = plt.subplots()

for c in df['class'].unique():
    df_class = df[df['class'] == c]
    ax.scatter(df_class['age'], df_class['fare'], c=colors[c], label=f'Class {c}')

plt.xlabel('Age')
plt.ylabel('Fare')
plt.title('Fare vs Age by Class')
plt.legend()
plt.show()



# How does this relationship change across the different classes?

# %%
