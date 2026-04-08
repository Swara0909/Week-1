import numpy as np
import pandas as pd

data=np.random.normal(loc=50, scale=0,size=1000)

df=pd.DataFrame(data, columns=['values'])

mean_val=data.mean()
std_dev=data.std()

def gaussian(x, mu, sigma):
    sigma = max(sigma, 1e-8)  # avoid zero
    return (1 / (sigma * (2 * np.pi) ** 0.5)) * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
x_values=np.linspace(min(data),max(data),1000)
y_values=gaussian(x_values,mean_val,std_dev)

print(gaussian(50,50,10))