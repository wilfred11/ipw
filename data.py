from causallib.datasets import load_nhefs
from causallib.estimation import IPW
from causallib.evaluation import evaluate
from sklearn.linear_model import LogisticRegression
from matplotlib import pyplot as plt


def get_data():
    data = load_nhefs()
    print(data.X.join(data.a).join(data.y))
    print(data.X)
    return data

def train_lr(data):
    learner = LogisticRegression(solver="liblinear")
    ipw = IPW(learner)
    ipw.fit(data.X, data.a)
    print(ipw.compute_weights(data.X, data.a).head())
    print(ipw.compute_weights(data.X, data.a).mean())