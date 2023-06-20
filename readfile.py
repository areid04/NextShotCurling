
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression

stra = r'C:\Users\alexr\PycharmProjects\NextShotCurling\output.xlsx'
df = pd.read_excel(stra)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import  Lasso

df = df.drop('refid',axis=1)
df = df[df['thrownx'] != 0]
df = df[(df['thrownx'] != 148) & (df['throwny'] != (588))]
df = df[(df['thrownx'] != 148) & (df['throwny'] != (589))]
df = df[(df['thrownx'] != 149) & (df['throwny'] != (588))]
df = df[(df['thrownx'] != 149) & (df['throwny'] != (589))]
print(df)
df['thrownx'] = 10 * round(df['thrownx'] / 10)
df['throwny'] = 10 * round(df['throwny'] / 10)
df = df[df['thrownx'] < 240]
df = df[df['thrownx'] > 40]
df = df[df['throwny'] > 130]
print(df.describe())
vars = df.drop('thrownx', axis=1)
vars = vars.drop('throwny', axis=1)
vars['edgetop'] = vars['e1']+vars['e2']+vars['e3']+vars['e4']
vars['edgebot'] = vars['e6']+vars['e5']
vars['innertop'] =vars['i1']+vars['i2']+vars['i3']+vars['i4']
vars['innerbot'] =vars['i5']+vars['i6']+vars['i7']+vars['i8']
vars['whitetop'] = vars['w1']+vars['w2']+vars['w3']+vars['w4']
vars['whitebot'] = vars['w5']+vars['w6']
vars['q1'] = vars['e1'] + vars['e2'] + vars['w1'] + vars['w2'] + vars['i1'] + vars['i2']
vars['q2'] = vars['e3'] + vars['e4'] + vars['w3'] + vars['w4'] + vars['i3'] + vars['i4']
vars['q3'] = vars['e5'] + vars['w5'] + vars['i5'] + vars['i6']
vars['q4'] =vars['e6'] + vars['w6'] + vars['i7'] + vars['i8']

X_train, X_test, y_train, y_test = train_test_split(vars, df[['thrownx','throwny']], test_size=0.25, random_state=42)
lr = Lasso(alpha=0.5)
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)
print("Coefficients: \n", lr.coef_)
print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
# The coefficient of determination: 1 is perfect prediction
print("Score: " + str(lr.score(X_test, y_test)))
print(r2_score(y_test,y_pred))