from causallib.datasets import load_nhefs
from causallib.estimation import IPW
from causallib.evaluation import evaluate
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

from matplotlib import pyplot as plt
#https://towardsdatascience.com/hands-on-inverse-propensity-weighting-in-python-with-causallib-14505ebdc109/

def train_lr(data):
    #learner = LogisticRegression()
    learner = RandomForestClassifier(n_estimators=1000)
    #learner = KNeighborsClassifier(n_neighbors=3)
    #clip_max=0.6798,clip_min=1-0.6798, verbose=True, use_stabilized=False
    ipw = IPW(learner)
    ipw.fit(data[['unemp_rate', 'technician_pc']],data['factory'])
    results = evaluate(ipw, data[['unemp_rate', 'technician_pc']], data['factory'],data['mean_income'], cv="auto")
    #print(ipw.compute_weights(data[['unemp_rate', 'technician_pc']],data['factory']).head())
    #print(ipw.compute_weights(data[['unemp_rate', 'technician_pc']],data['factory']))
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    results.plot_covariate_balance(kind="love", ax=ax, thresh=0.1)
    plt.show()

    from sklearn import metrics
    metrics = {"roc_auc": metrics.roc_auc_score,
               "avg_precision": metrics.average_precision_score, }
    #ipw = IPW(LogisticRegression(solver="liblinear"))
    #results = evaluate(ipw, data.X, data.a, data.y, cv="auto", metrics_to_evaluate=metrics)
    results.plot_all()
    plt.show()
    #outcomes = ipw.estimate_population_outcome(data[['unemp_rate', 'technician_pc']],data['factory'], data['mean_income'])
    #print(outcomes)