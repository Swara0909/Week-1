from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.datasets import load_iris

data=load_iris()

X=data.data
y=data.target

X_train, X_test, y_train, y_test=train_test_split(X,y,test_size=0.2)

model=DecisionTreeClassifier(criterion='gini', max_depth=3)
model1=DecisionTreeRegressor(max_depth=3)

model.fit(X_train, y_train)
model1.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)
y_predicted=model1.predict(X_test)

# Accuracy
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Regression MSE:", mean_squared_error(y_test, y_predicted))

from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
plot_tree(model, filled=True)
plt.show()