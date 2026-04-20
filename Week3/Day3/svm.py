# For classification

from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score

# Load dataset
data = load_iris()
X = data.data
y = data.target

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create model
model = SVC(kernel='linear')   # try 'rbf', 'poly' also

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
print("Accuracy:", accuracy_score(y_test, y_pred))


# For Regression

from sklearn.svm import SVR
import numpy as np
from sklearn.metrics import mean_squared_error

# Sample data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([5, 10, 15, 20, 25])

# Model
model = SVR(kernel='linear')

# Train
model.fit(X, y)

# Predict
y_pred = model.predict([[6]])

print("Prediction:", y_pred)
print("MSE:", mean_squared_error([30], y_pred))