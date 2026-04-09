import pandas as pd

df=pd.DataFrame({
    "marks":[80,90,70,60,85],
    "hours":[4,5,3,2,6]
})

subset=df[df["hours"]>3]
prob=(subset['marks']>75).mean()
print(prob)


