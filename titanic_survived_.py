# -*- coding: utf-8 -*-
"""Titanic survived .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QxvIMW8_pGlQMMc-teQN_OmAsc0xyQBs
"""

import numpy as np
import pandas as pd
import matplotlib as mlp
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn

df = pd.read_csv('train.csv')
df.head()

df.shape

df.describe()

df.isnull().sum()

df.duplicated().sum()

df['Age']= df['Age'].fillna(df['Age'].mean())
df[['Embarked', 'Cabin']]= df[['Embarked', 'Cabin']].ffill()
null_vals_after = df.isna().sum()
null_vals_after

df =df.dropna()
null_vals_after = df.isna().sum()
null_vals_after

df.columns

labels = df.pop('Survived')

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(df, labels, test_size=0.25)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
x_train['Name'] = le.fit_transform(x_train['Name'])
x_test['Name'] = le.fit_transform(x_test['Name'])
object_cols = x_train.select_dtypes(include='object').columns
for col in object_cols:
    x_train[col] = le.fit_transform(x_train[col])
    x_test[col] = le.fit_transform(x_test[col])
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

from sklearn.metrics import roc_auc_score
roc_auc_score(y_test, y_pred)

from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

n_estimators = [2,4,6,8,16,32,64,100,200]
train_results = []
test_results = []

for estimator in n_estimators:
    model = RandomForestClassifier(n_estimators=estimator, n_jobs = -1)
    model.fit(x_train, y_train)
    train_pred = model.predict(x_train)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_train, train_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    train_results.append(roc_auc)
    y_pred = model.predict(x_test)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    test_results.append(roc_auc)

line1, = plt.plot(n_estimators, train_results, 'b', label='Train AUC')
line2, = plt.plot(n_estimators, test_results, 'r', label='Test AUC')
plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('AUC score')
plt.xlabel('n_estimators')
plt.show()

