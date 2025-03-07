import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler




X = np.load('path/to/X_[MODALITY].npy')
y = np.load('path/to/y_[MODALITY].npy')

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

svm_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', SVC(probability=True))
])

param_space = {
    'svm__C': Real(0.1, 100, prior='log-uniform'),
    'svm__gamma': Real(0.01, 10, prior='log-uniform'),
    'svm__kernel': Categorical(['rbf', 'linear', 'poly']),
    'svm__degree': Integer(1, 5),
    'svm__class_weight': Categorical([None, 'balanced'])
}

opt = BayesSearchCV(
    svm_pipeline,
    search_spaces=param_space,
    n_iter=32,
    cv=3,
    scoring='accuracy',
    n_jobs=-1,
    random_state=42
)

opt.fit(X_train, y_train)

print("Best hyperparameters found: ", opt.best_params_)

y_pred_prob = opt.predict_proba(X_test)[:, 1]
y_pred = (y_pred_prob > 0.5).astype(int)

auc_score = roc_auc_score(y_test, y_pred_prob)
report = classification_report(y_test, y_pred, target_names=['Class 0', 'Class 1'])

print("AUC Score:", auc_score)
print(report)