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

The link above uses a minimal example to explain how, by weighting individual records, IPW balances a dataset. In the example at hand it doubles the number of results in the dataset. By doubling the results, the technique somehow falsifies results obtained from studies. In the example this falsification problem is handled. After applying the IPW technique, the sex of an individual no longer has influence on its chance to receive the treatment, while on beforehand a female had 75% chance to receive treatment. This gives way to the illustration in which the vertex between sex and treatment is removed.

<img src="https://github.com/user-attachments/assets/c6e72a9d-53d6-46e3-b56e-613b42e2df38" alt="drawing" width="200"/>
<img src="https://github.com/user-attachments/assets/57ae1a48-ebf5-4cc2-9cbe-d2a66c46d1ad" alt="drawing" width="200"/>

#### Case study

To test the ideas of IPW ourself, I have used IPW on [a kaggle dataset](https://www.kaggle.com/datasets/rkiattisak/student-performance-in-mathematics). 

For every student the dataset contains social, gender, racial indicators, some test results and whether or not a test preparation course was followed.

At first data needs to be inspected and prepared, for categorical data dummy binary columns need to be created (IPW is all about numbers).

The social, gender, racial indicators will be used to get an idea of how likely someone is to take the test preparation course. The dependent variable is the result on a math test.

To find out how interesting it would be to take a test preparation course, the Python causallib library was used to calculate a treatment effect.

The propensity scores are calculated using sklearn's LogisticRegression learner. CausalLib IPW model is then used to assign a weight to every record. A higher weight on a student that is in the treated group would indicate only a few students in the treated group are having similar confounders (the social, gender and racial indicators). 

##### Propensity score histogram

Before getting actual results it is interesting to get an idea of treated and untreated students and their propensity scores.

![prop-hist](https://github.com/user-attachments/assets/0b467309-5ce4-4101-9ca1-d801f71184cf)

From the image above it is to be seen there is a lot of overlap between the group that took the test preparation course and the group that did not. So every type of student that did take the course, has a counterpart that didn't take it. The image also makes clear that the majority of students didn't take the course.

##### Results
The ATE is obtained as follows. The x-cols variable contains all the confounders.

`from causallib.estimation import IPW`

`from sklearn.linear_model import LogisticRegression`

`learner = LogisticRegression()`

`ipw = IPW(learner)`

`x-cols= ['standard', 'group B', 'group C', 'group D', 'group E', "associate's degree", "bachelor's degree", "high school", "master's degree", "some high school", 'female']`

`outcomes = ipw.estimate_population_outcome(data[x_cols], data['test preparation course'], data['math score'])`

`effect = ipw.estimate_effect(outcomes[1], outcomes[0])`

The effect is 5.54, so taking the test preparation course increases the math score by 5.54 points. The maximum score to be obtained for the math test is 100.

##### Assessment

The weighting has had its effects on the covariates, after weighting there is hardly any difference between them.

![love](https://github.com/user-attachments/assets/308ad93a-5d3b-4466-903c-2f148d2020b9)

This graph shows the distribution of propensity scores over the treated and untreated group after weighting. The distribution shows a balanced distribution, which is good.

![propensity_distr](https://github.com/user-attachments/assets/571f5331-8ed6-449d-8260-b07fdf2ac8ca)

























