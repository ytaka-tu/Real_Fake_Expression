import numpy as np
import os
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import sys
from xgboost import XGBClassifier
import sklearn
from sklearn.linear_model.stochastic_gradient import SGDClassifier
from sklearn import ensemble
from sklearn import cross_validation
import pickle
X = []
y = []
X_test = []
y_test = []
trainPath = '../results_sadness/'

classes = ['N2S.npy','H2N2S.npy']
classesName = {}
classesName[classes[0]] = 0
classesName[classes[1]] = 1

subjects = range(1,41)
train,test = cross_validation.train_test_split(subjects, train_size = 0.9, random_state=1)

trainSubjects = os.listdir(trainPath)
for subject in trainSubjects:
	x = np.load(trainPath + subject)
	filename = subject.split("_")[1]
	su = int(subject.split("_")[0])
	if su in train:
		X.append(x.flatten().tolist())
		y.append(classesName[filename])
	else:
		X_test.append(x.flatten().tolist())
		y_test.append(classesName[filename])


X = np.array(X)
y = np.array(y)
X_test = np.array(X_test)
y_test = np.array(y_test)
eval_set = [(X, y), (X_test, y_test)]


model = XGBClassifier(learning_rate=0.0075,silent=True,n_estimators=4500,subsample=1,reg_lambda=100)
model.fit(X, y, early_stopping_rounds=4500,eval_metric="error", eval_set=eval_set, verbose=False)


pickle.dump(model, open("../../sadness/model.dat","wb"))






