import pandas as pd

df = pd.DataFrame({
    "spam": [1,1,0,1,0],
    "link": [0,0,1,1,1]
})

# P(spam)
p_spam = df["spam"].mean()

# P(link | spam)
p_link_given_spam = df[df["spam"]==1]["link"].mean()

# P(link)
p_link = df["link"].mean()

# Bayes Theorem
p_spam_given_link = (p_link_given_spam * p_spam) / p_link

print("P(spam):", p_spam)
print("P(link | spam):", p_link_given_spam)
print("P(spam | link):", p_spam_given_link)