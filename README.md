### Propensity Score Matching

The "propensity score" describes how likely a unit is to have been treated, given its covariate values. Data that is not obtained using a randomized controlled trial (RCT) is usually much harder to compare, or it is harder to draw almost causal conclusions from. Using a technique like "propensity score matching", it gets easier to obtain clearer results without going through all the formalities of a RCT. Sometimes it is just the only way to get some idea off the effects a decision has.

The example I use here, is a very limited example that could have been used in some earlier stage of development, where factories should be view as workplaces.

#### Simple case
Suppose for example a simple case where a company builds factories in villages. To naively compare the effects of the factory on village income a simple weighted mean difference between income with and without factory has to be made. This could lead to the conclusion that the mean income of a village lowers after building a factory nearby.

![naive](https://github.com/user-attachments/assets/779a2a92-69d3-412c-9985-0b2406054fab)

#### Still a simple case

A better way to compare differences in income for villages with and without factories would be to only compare villages that would be good candidates for building a factory. For this reason the features used to select villages apt for building a factory should be used to find which villages with factories match villages without factories. In this case the unemployment rate and the number of technicians per capita are used to assert whether villages are apt to build a factory nearby. The number of technicians in a village gives an idea of how self-sustainable a village is. In this case the matches are made by hand. And the records that have no match are excluded from effect calculations. Average Treatment Effect of the Treated calculated according to this method is probably a better measure than the calculations in the simple case.

![less-naive](https://github.com/user-attachments/assets/c7755d42-09e5-45dd-ab9f-d2dd161bdf73)



#### The propensity score

Using logistic regression one could find one score per individual village. This score, that captures all features on which a village is selected, makes it possible to match records automatically, and is more accurate than handpicking records. The image shows all selected records have matches with record 11 and record 12, so record 11 and 12 form the control group. So the treatment effect is obtained using only two records for villages where no factory has been build.

![prop](https://github.com/user-attachments/assets/41c71a19-e48c-4774-b729-afcf693fdd94)

The way to calculate propensity scores would be to use the following code, in this case.

`from sklearn.linear_model import LogisticRegression`

`model = LogisticRegression().fit(data[['unemp_rate', 'technician_pc']],data['factory'] )`

To get the scores themselves is done using the following line of code. 

`model.predict_proba(d_full[['unemp_rate', 'technician_pc']])[:,1]`

### Inverse propensity weighting

[To understand why to use IPW](https://towardsdatascience.com/understanding-inverse-probability-of-treatment-weighting-iptw-in-causal-inference-4e69692bce7e/)

The link above uses a minimal example to explain how, by weighting individual records, biases are removed in such a way that the influence of having knowledge on someone's sex provides knowledge in whether or not someone received a treatment. The technique creates a pseudopopulation in the example at hand, it doubles the number of results in the dataset. In this way this technique somehow falsifies results obtained from studies, it also shows how to adress these problems.

The link above explains how IPW balances the data in such a way that knowing the sex of a individual has no influence on its chance to receive the treatment.

Sex affects the outcome but it no longer affects the treatment.

![confound](https://github.com/user-attachments/assets/c6e72a9d-53d6-46e3-b56e-613b42e2df38)

![unconfound](https://github.com/user-attachments/assets/57ae1a48-ebf5-4cc2-9cbe-d2a66c46d1ad)
















