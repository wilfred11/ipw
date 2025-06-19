import numpy as np
import pandas as pd
from causallib.estimation import IPW
from causallib.evaluation import evaluate
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression

def get_dummies(data):
    lunch_dummy = pd.get_dummies(data['lunch'])
    race_dummy = pd.get_dummies(data['race/ethnicity'])
    par_edu_dummy = pd.get_dummies(data['parental level of education'])
    gender_dummy = pd.get_dummies(data['gender'])
    data_dummified = pd.concat([data, lunch_dummy, race_dummy, par_edu_dummy, gender_dummy], axis=1).drop(['free/reduced', 'lunch', 'race/ethnicity','group A', 'parental level of education', 'some college', 'gender', 'male'], axis=1)

    data_dummified['test preparation course'] = np.where(data_dummified['test preparation course'] == 'completed', True, False)

    return data_dummified


def get_exams_data():
    exam_data = pd.read_csv("data/exams.csv")
    print(exam_data.head())
    print(exam_data.describe())
    print(exam_data.columns)
    print("length dataset:"+str(len(exam_data)))
    s = exam_data.duplicated().unique()
    if not s[0] & len(s)==1:
        print("duplicates?:no")

    result = exam_data.isnull().values.any()
    print(result)
    result = exam_data.notna().values.all()
    print(result)
    print(exam_data.dtypes)
    unique_values = exam_data.apply(pd.Series.unique)
    print(unique_values)
    return exam_data

def ipw(data):
    learner = LogisticRegression()
    #learner = RandomForestClassifier(n_estimators=1000)
    # learner = KNeighborsClassifier(n_neighbors=3)
    # clip_max=0.6798,clip_min=1-0.6798, verbose=True, use_stabilized=False
    ipw = IPW(learner)
    ipw.fit(data[x_columns()], data['test preparation course'])
    results = evaluate(ipw, data[x_columns()], data['test preparation course'], data['math score'], cv="auto", plots=True )
    # print(ipw.compute_weights(data[['unemp_rate', 'technician_pc']],data['factory']).head())
    # print(ipw.compute_weights(data[['unemp_rate', 'technician_pc']],data['factory']))
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    results.plot_covariate_balance(kind="love", ax=ax, thresh=0.1)
    plt.show()

def x_columns():
    return ['standard', 'group B', 'group C', 'group D', 'group E',
       "associate's degree", "bachelor's degree", "high school",
       "master's degree", "some high school", 'female']

def a_columns():
    return ['test preparation course']





