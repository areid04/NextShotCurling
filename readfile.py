import random
import numpy as np
import tensorflow as tf
random.seed(42)
np.random.seed(42)
tf.random.set_seed(42)
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression

stra = r'C:\Users\alexr\PycharmProjects\NextShotCurling\outputupd3back.xlsx'
df = pd.read_excel(stra)
print(len(df))
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import  Lasso
from sklearn.pipeline import  make_pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import AdaBoostRegressor
df = df.dropna()
df = df.drop('refid',axis=1)
df = df[df['thrownx'] != 0]
df = df[(df['thrownx'] != 148) & (df['throwny'] != (588))]
df = df[(df['thrownx'] != 148) & (df['throwny'] != (589))]
df = df[(df['thrownx'] != 149) & (df['throwny'] != (588))]
df = df[(df['thrownx'] != 149) & (df['throwny'] != (589))]
df['thrownx'] = 10 * round(df['thrownx'] / 10)
df['throwny'] = 10 * round(df['throwny'] / 10)
df = df[df['thrownx'] < 280]
df = df[df['thrownx'] > 20]
df = df[df['throwny'] > 100]
df = df[df['throwny'] < 560]
print(len(df))
vars = df.drop('thrownx', axis=1)
vars = vars.drop('throwny', axis=1)
vars['edgetop'] = vars['ei1']+vars['ei2']+vars['ei3']+vars['ei4']+vars['eo1']+vars['eo2']+vars['eo3']+vars['eo4']+vars['ei5']+vars['ei6']+vars['ei7']+vars['ei8']+vars['eo6']+vars['eo7']+vars['eo8']
vars['edgebot'] = vars['ei9']+vars['ei10']+vars['ei11']+vars['ei12']+vars['eo9']+vars['eo10']+vars['eo11']+vars['eo12']+vars['ei13']+vars['ei14']+vars['ei15']+vars['ei16']+vars['eo13']+vars['eo14']+vars['eo15']+vars['eo16']
vars['innertop'] =vars['i1']+vars['i2']+vars['i3']+vars['i4']+vars['i5']+vars['i6']+vars['i7']+vars['i8']
vars['innerbot'] =vars['i9']+vars['i10']+vars['i11']+vars['i12']+vars['i13']+vars['i14']+vars['i15']+vars['i16']
vars['whitetop'] = vars['wi1']+vars['wi2']+vars['wi3']+vars['wi4']+vars['wo1']+vars['wo2']+vars['wo3']+vars['wo4']+vars['wi5']+vars['wi6']+vars['wi7']+vars['wi8']+vars['wo6']+vars['wo7']+vars['wo8']

vars['whitebot'] = vars['wi9']+vars['wi10']+vars['wi11']+vars['wi12']+vars['wo9']+vars['wo10']+vars['wo11']+vars['wo12']+vars['wi13']+vars['wi14']+vars['wi15']+vars['wi16']+vars['wo13']+vars['wo14']+vars['wo15']+vars['wo16']

vars['q1'] = vars['ei1']+vars['ei2']+vars['ei3']+vars['ei4']+vars['eo1']+vars['eo2']+vars['eo3']+vars['eo4']+vars['i1']+vars['i2']+vars['i3']+vars['i4']+vars['wi1']+vars['wi2']+vars['wi3']+vars['wi4']+vars['wo1']+vars['wo2']+vars['wo3']+vars['wo4']
vars['q2'] = vars['ei5']+vars['ei6']+vars['ei7']+vars['ei8']+vars['eo6']+vars['eo7']+vars['eo8']+vars['i5']+vars['i6']+vars['i7']+vars['i8']+vars['wi5']+vars['wi6']+vars['wi7']+vars['wi8']+vars['wo6']+vars['wo7']+vars['wo8']
vars['q3'] = vars['ei9']+vars['ei10']+vars['ei11']+vars['ei12']+vars['eo9']+vars['eo10']+vars['eo11']+vars['eo12']+vars['i9']+vars['i10']+vars['i11']+vars['i12']+vars['wi9']+vars['wi10']+vars['wi11']+vars['wi12']+vars['wo9']+vars['wo10']+vars['wo11']+vars['wo12']
vars['q4'] = vars['ei13']+vars['ei14']+vars['ei15']+vars['ei16']+vars['eo13']+vars['eo14']+vars['eo15']+vars['eo16']+vars['wi13']+vars['wi14']+vars['wi15']+vars['wi16']+vars['wo13']+vars['wo14']+vars['wo15']+vars['wo16']
X_train, X_test, y_train, y_test = train_test_split(vars, df['thrownx'], test_size=0.25, random_state=42)
# training the x co-ord
from sklearn.preprocessing import StandardScaler
lr = RandomForestRegressor(n_estimators=200,criterion='friedman_mse',max_features=6,bootstrap=True,random_state=42,min_samples_split=2,min_samples_leaf=2,ccp_alpha=0.00001)
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)
print("Mean absolute error: %.2f" % mean_absolute_error(y_test, y_pred))
# The coefficient of determination: 1 is perfect prediction
print("Score: " + str(lr.score(X_test, y_test)))
print(r2_score(y_test,y_pred))

print(lr.predict(vars.iloc[[2]]))
# training the y-cord
X_trainy, X_testy, y_trainy, y_testy = train_test_split(vars, df['throwny'], test_size=0.25, random_state=42)
from sklearn.preprocessing import StandardScaler
lry = RandomForestRegressor(n_estimators=100,criterion='absolute_error',max_features=6,random_state=42,min_weight_fraction_leaf=0.0000000002,min_samples_split=2,min_samples_leaf=2,ccp_alpha=0.000001)
ssy = StandardScaler()
X_trainy = ssy.fit_transform(X_trainy)
X_testy = ssy.transform(X_testy)
lry.fit(X_trainy, y_trainy)
y_predy = lry.predict(X_testy)
print("Mean absolute error: %.2f" % mean_absolute_error(y_testy, y_predy))
# The coefficient of determination: 1 is perfect prediction
print("Score: " + str(lry.score(X_testy, y_testy)))
print(r2_score(y_testy,y_predy))

print(lry.predict(vars.iloc[[2]]))
