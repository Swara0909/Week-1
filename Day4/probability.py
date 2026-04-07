import numpy as np

# probability of 6
dice=np.random.randint(1,7,1000)
prob_6=np.sum(dice==6)/len(dice)
print(prob_6)

# probability of even numbers
data=np.random.randint(1,11,1000)
prob_even=np.sum(data%2==0)/len(data)
print(prob_even)

# conditional probability

# P(Even|number>5)
data=np.random.randint(1,11,1000)
A=data%2==0
B=data>5
prob=np.sum(A&B)/np.sum(B)
print(prob)

import pandas as pd

df = pd.DataFrame({
    'spam': [1, 0, 1, 1, 0],
    'contains_link': [1, 0, 1, 0, 1]
})

# P(spam = 1)
p_spam = df['spam'].mean()

# P(link = 1 | spam = 1)
p_link_given_spam = df[df['spam'] == 1]['contains_link'].mean()
print(p_spam, p_link_given_spam)