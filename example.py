import pandas as pd
from sklearn.linear_model import LogisticRegression

def simple_data():
    print("Company decides to built factories in several villages. The presence of a factory in a village seems to lower  income")
    d = pd.DataFrame({'factory': [1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0], 'mean_income': [11,9,14,11,15,12,14,23, 17,4,8,6, 10,15,22,19]})

    count_1 = d['factory'].value_counts().get(1, 0)
    count_0 = d['factory'].value_counts().get(0, 0)
    print("Occurrences of '1':", count_1)
    print("Occurrences of '0':", count_0)

    factory_rows = d[d['factory']==1]
    no_factory_rows = d[d['factory'] == 0]
    factory_rows_= factory_rows['mean_income'].sum()/count_1
    no_factory_rows_ = no_factory_rows['mean_income'].sum() / count_0
    print(d)
    print("ATE: "+str(factory_rows_- no_factory_rows_))

    print("Company decides to built factories in several villages. Factories are built near villages that have a certain unemployment rate and a number of technicians per capita")
    print("Propensity score matching is about comparing the treated individuals to untreated individuals having similar scores for unemployment rate and the number of technicians per capita (or whatever features are used to select individuals).")
    print("Only data that is treated or that matches the treated group is used to calculate a resulting ATE (average treatment effect, the ATE is better in calculated this way.")
    d_full = pd.DataFrame({'factory': [1,1,1,1,1,1,1,1, 1, 1, 1, 0, 0, 0, 0, 0], 'mean_income': [11,9,14,11,15,12,14,23, 17, 4, 8, 6, 10, 15, 22, 19],
                      'unemp_rate': [0.16,0.15,0.16,0.15,0.17,0.16,0.13,0.16, 0.18, 0.17, 0.15, 0.15, 0.17, 0.03, 0.03, 0.04],
                      'technician_pc': [0.14,0.13,0.13,0.12,0.13,0.13,0.12,0.15, 0.13, 0.14, 0.14, 0.14, 0.13, 0.01, 0.02, 0.02],
                       'self_match':[11,11,12,11,12,12,11,12,12,12, 11,0,0,0,0,0]})

    print(d_full)
    print("ATE: " + str(factory_rows_ - (90/11)))

    print("In ML it is more appropriate to use an classifier like logistic regression to get values that match. Using LogisticRegression it is easier to find matching records.")
    model = LogisticRegression(max_iter=10000).fit(d_full[['unemp_rate', 'technician_pc']],d_full['factory'] )
    #p=model.coef_.ravel()[:1]
    #print(p)
    print(model.predict_proba(d_full[['unemp_rate', 'technician_pc']])[:, 1])



    d_full1 = pd.DataFrame({'factory': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                           'mean_income': [11, 9, 14, 11, 15, 12, 14, 23, 17, 4, 8, 6, 10, 15, 22, 19],
                           'unemp_rate': [0.16, 0.15, 0.16, 0.15, 0.17, 0.16, 0.13, 0.16, 0.18, 0.17, 0.15, 0.15, 0.17,
                                          0.03, 0.03, 0.04],
                           'technician_pc': [0.14, 0.13, 0.13, 0.12, 0.13, 0.13, 0.12, 0.15, 0.13, 0.14, 0.14, 0.14,
                                             0.13, 0.01, 0.02, 0.02],
                           'self_match': [11, 11, 12, 11, 12, 12, 11, 12, 12, 12, 11, 0, 0, 0, 0, 0],
                           'propensity': model.predict_proba(d_full[['unemp_rate', 'technician_pc']])[:,1],
                           'propensity_round': model.predict_proba(d_full[['unemp_rate', 'technician_pc']])[:,1].round(4)
                           }
                          )
    no_fact = d_full1[d_full1['factory'] == 0]
    fact = d_full1[d_full1['factory'] == 1]
    #print(no_fact.index.values)
    matches=[]

    for r in fact['propensity_round']:
        l = []
        for m in no_fact['propensity_round']:
            l.append(abs(r-m))
        #print(l)
        min_index= l.index(min(l))
        #print(min_index)
        matches.append(no_fact.index.values[min_index])
    print(matches)
    print(len(no_fact))
    for i in no_fact['propensity']:
        print(i)
        matches.append(-1)
    print(len(matches))
    d_full1['prop_match']= matches
    print(d_full1)
    print("ATE: " + str(factory_rows_ - (86 / 11)))
    return d
