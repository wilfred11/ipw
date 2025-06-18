from data import get_data, train_lr
from example import simple_data

#https://towardsdatascience.com/hands-on-inverse-propensity-weighting-in-python-with-causallib-14505ebdc109/

do=2

if do==1:
    d=get_data()
    train_lr(d)

if do==2:
    simple_data()
