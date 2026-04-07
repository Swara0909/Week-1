import numpy as np
import pandas as pd

data = pd.DataFrame({
    'marks': [50, 60, 70, 80, 90],
    'study_hours': [2, 3, 4, 5, 6]
})

print("Data:\n", data)

# Mean & Standard Deviation
mean_marks = data['marks'].mean()
std_marks = data['marks'].std()

print("\nMean Marks:", mean_marks)
print("Std Dev Marks:", std_marks)

# Z-score Normalization
z_scores = (data['marks'] - mean_marks) / std_marks
print("\nZ-scores:\n", z_scores)

# Probability
# P(marks > 70)
prob_high = len(data[data['marks'] > 70]) / len(data)
print("\nP(marks > 70):", prob_high)

# Conditional Probability
# P(marks > 70 | study_hours > 3)
subset = data[data['study_hours'] > 3]
prob_cond = len(subset[subset['marks'] > 70]) / len(subset)

print("P(marks > 70 | study_hours > 3):", prob_cond)

# 6. Correlation
corr = data['marks'].corr(data['study_hours'])
print("\nCorrelation:", corr)