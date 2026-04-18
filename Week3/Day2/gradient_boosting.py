# For Classification

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits

SEED=23

X,y=load_digits(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=SEED, test_size=0.2)

model=GradientBoostingClassifier(learning_rate=0.05, n_estimators=300, max_features=5, random_state=100)

model.fit(X_train, y_train)

y_pred=model.predict(X_test)

acc = accuracy_score(y_test, y_pred)
print("Gradient Boosting Classifier accuracy is : {:.2f}".format(acc))

# For Regression

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.datasets import load_digits

SEED=23

X,y=load_digits(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=SEED, test_size=0.2)

model=GradientBoostingRegressor(learning_rate=0.05, n_estimators=300, max_features=5, random_state=100)

model.fit(X_train, y_train)

y_pred=model.predict(X_test)

MSE = mean_squared_error(y_test, y_pred)
print("Gradient Boosting Regression MSE is : {:.2f}".format(acc))


