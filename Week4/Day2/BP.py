import numpy as np
import pandas as pd


## creating a sample data
df = pd.DataFrame([[8,8,4],[7,9,5],[6,10,6],[5,12,7]],columns=['cgpa','profile_score','lpa'])

df

## intialize w,b,layer dim
def intialize_parameters(layer_dims):

  np.random.seed(3)
  parameters ={}
  L = len(layer_dims)
  for l in range(1,L):
    parameters['W' + str(l)] = np.ones((layer_dims[l-1],layer_dims[l]))*0.1
    parameters['b' + str(l)] = np.zeros((layer_dims[l],1))
  return parameters
