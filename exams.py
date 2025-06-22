import numpy as np
import pandas as pd
from causallib.estimation import IPW
from causallib.evaluation import evaluate
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, cross_val_score, StratifiedKFold


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
    learner = LogisticRegression(max_iter=1000, random_state=21)
    ipw = IPW(learner, clip_min=0.05, clip_max=0.95)
    ipw.fit(data[x_columns()], data['test preparation course'])
    k_fold = StratifiedKFold(n_splits=2, random_state=21, shuffle=True)
    k_fold_splits =  k_fold.split(data[x_columns()], data['test preparation course'], groups=None)
    results = evaluate(ipw, data[x_columns()], data['test preparation course'], data['math score'], cv=k_fold_splits)

    print(ipw.compute_weights(data[x_columns()], data['test preparation course']).head())

    outcomes = ipw.estimate_population_outcome(data[x_columns()], data['test preparation course'], data['math score'])
    print(outcomes)
    effect = ipw.estimate_effect(outcomes[1], outcomes[0])
    print(effect)

    print(ipw.compute_propensity_matrix(data[x_columns()], data['test preparation course']))
    hist=ipw.compute_propensity_matrix(data[x_columns()], data['test preparation course'])
    hist['test preparation course']= data['test preparation course']
    hist_treated = hist[hist['test preparation course']==True]
    hist_untreated = hist[hist['test preparation course'] == False]
    plt.hist(hist_treated[True],
             alpha=0.5,
             label='test preparation course', bins=10)

    plt.hist(hist_untreated[True],
             alpha=0.5,
             label='no test preparation course(CG)', bins=10)

    plt.legend(loc='upper right')
    plt.title('Propensity scores histogram')
    plt.legend()
    plt.savefig("out/ipw/prop_histo")
    plt.clf()


    fig, [a0, a1] = plt.subplots(1, 2, figsize=(12, 6))
    results.plot_covariate_balance(kind="love", phase="train", ax=a0, thresh=0.1)
    results.plot_covariate_balance(kind="love", phase="valid", ax=a1, thresh=0.1)
    for ax, suffix in [(a0, "Train"), (a1, "Validation")]:
        ax.set_title(ax.get_title() + ": " + suffix)
    plt.tight_layout()
    plt.savefig("out/ipw/love")
    plt.clf()

    fig, [a0, a1] = plt.subplots(1, 2, figsize=(12, 6))
    results.plot_covariate_balance(kind="slope", phase="train", ax=a0, thresh=0.1)
    results.plot_covariate_balance(kind="slope", phase="valid", ax=a1, thresh=0.1)
    for ax, suffix in [(a0, "Train"), (a1, "Validation")]:
        ax.set_title(ax.get_title() + ": " + suffix)
    plt.tight_layout()
    plt.savefig("out/ipw/slope")
    plt.clf()

    fig, [a0, a1] = plt.subplots(1, 2, figsize=(12, 6))
    results.plot_weight_distribution(reflect=True, ax=a0)
    results.plot_weight_distribution(reflect=True, phase="valid", ax=a1)
    for ax, suffix in [(a0, "Train"), (a1, "Validation")]:
        ax.set_title(ax.get_title() + ": " + suffix)
    plt.tight_layout()
    plt.savefig("out/ipw/weight_distri")
    plt.clf()

    fig, [a0, a1] = plt.subplots(1, 2, figsize=(12, 6))
    results.plot_roc_curve(ax=a0)
    results.plot_roc_curve(phase="valid", ax=a1)
    for ax, suffix in [(a0, "Train"), (a1, "Validation")]:
        ax.set_title(ax.get_title() + ": " + suffix)
    plt.tight_layout()
    plt.savefig("out/ipw/roc")
    plt.clf()

    fig, [a0, a1] = plt.subplots(1, 2, figsize=(12, 6))
    results.plot_pr_curve(ax=a0)
    results.plot_pr_curve(phase="valid", ax=a1)
    for ax, suffix in [(a0, "Train"), (a1, "Validation")]:
        ax.set_title(ax.get_title() + ": " + suffix)
    plt.tight_layout()
    plt.savefig("out/ipw/pr")
    plt.clf()


def x_columns():
    return ['standard', 'group B', 'group C', 'group D', 'group E',
       "associate's degree", "bachelor's degree", "high school",
       "master's degree", "some high school", 'female']

def a_columns():
    return ['test preparation course']





