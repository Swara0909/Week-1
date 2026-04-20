# For classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score

# Load dataset
data = load_iris()
X = data.data
y = data.target

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
model = RandomForestClassifier(n_estimators=100, max_depth=3)

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
print("Accuracy:", accuracy_score(y_test, y_pred))

# For Regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Sample data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([5, 10, 15, 20, 25])

# Model
model = RandomForestRegressor(n_estimators=100, max_depth=3)

# Train
model.fit(X, y)

# Predict
y_pred = model.predict([[6]])

print("Prediction:", y_pred)
print("MSE:", mean_squared_error([30], y_pred))