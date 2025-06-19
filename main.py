from c_lib import train_lr
from example import simple_data, get_less_simple_data
from exams import get_exams_data, ipw, get_dummies

#https://towardsdatascience.com/hands-on-inverse-propensity-weighting-in-python-with-causallib-14505ebdc109/

#https://towardsdatascience.com/hands-on-inverse-propensity-weighting-in-python-with-causallib-14505ebdc109/

#https://towardsdatascience.com/understanding-inverse-probability-of-treatment-weighting-iptw-in-causal-inference-4e69692bce7e/

do=3

if do==1:
    simple_data()

if do==2:
    d=get_less_simple_data()
    train_lr(d)

if do == 3:
    data = get_exams_data()
    dummified_data = get_dummies(data)
    print(dummified_data.columns)
    print(dummified_data.head())
    ipw(dummified_data)






