from example import simple_data, get_less_simple_data
from exams import get_exams_data, ipw, get_dummies
from why import test

#https://towardsdatascience.com/hands-on-inverse-propensity-weighting-in-python-with-causallib-14505ebdc109/

#https://towardsdatascience.com/hands-on-inverse-propensity-weighting-in-python-with-causallib-14505ebdc109/

#https://towardsdatascience.com/understanding-inverse-probability-of-treatment-weighting-iptw-in-causal-inference-4e69692bce7e/

#https://medium.com/@med.hmamouch99/exploring-causal-inference-with-dowhy-24176444c457

do=3

if do==1:
    simple_data()

if do == 2:
    data = get_exams_data()
    dummified_data = get_dummies(data)
    print(dummified_data.columns)
    print(dummified_data.head())
    ipw(dummified_data)

if do ==3:
    data = get_exams_data()
    print(data.columns)
    test(data)







