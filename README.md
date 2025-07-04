## Propensity Score Matching

The "propensity score" describes how likely a unit is to have been treated, given its covariate values. Data that is not obtained using a randomized controlled trial (RCT) is usually much harder to compare, or it is harder to draw almost causal conclusions from. Using a technique like "propensity score matching", it gets easier to obtain clearer results without going through all the formalities of a RCT. Sometimes it is just the only way to get some idea off the effects a decision has.

The example I use here, is a very limited example that could have been used in some earlier stage of development, where factories should be view as workplaces.

### Simple case
Suppose for example a simple case where a company builds factories in villages. To naively compare the effects of the factory on village income a simple weighted mean difference between income with and without factory has to be made. This could lead to the conclusion that the mean income of a village lowers after building a factory nearby.

![naive](https://github.com/user-attachments/assets/779a2a92-69d3-412c-9985-0b2406054fab)

### Still a simple case

A better way to compare differences in income for villages with and without factories would be to only compare villages that would be good candidates for building a factory. For this reason the features used to select villages apt for building a factory should be used to find which villages with factories match villages without factories. In this case the unemployment rate and the number of technicians per capita are used to assert whether villages are apt to build a factory nearby. The number of technicians in a village gives an idea of how self-sustainable a village is. In this case the matches are made by hand. And the records that have no match are excluded from effect calculations. Average Treatment Effect of the Treated calculated according to this method is probably a better measure than the calculations in the simple case.

![less-naive](https://github.com/user-attachments/assets/c7755d42-09e5-45dd-ab9f-d2dd161bdf73)



### The propensity score

Using logistic regression one could find one score per individual village. This score, that captures all features on which a village is selected, makes it possible to match records automatically, and is more accurate than handpicking records. The image shows all selected records have matches with record 11 and record 12, so record 11 and 12 form the control group. So the treatment effect is obtained using only two records for villages where no factory has been build.

![prop](https://github.com/user-attachments/assets/41c71a19-e48c-4774-b729-afcf693fdd94)

The way to calculate propensity scores would be to use the following code, in this case.

`from sklearn.linear_model import LogisticRegression`

`model = LogisticRegression().fit(data[['unemp_rate', 'technician_pc']],data['factory'] )`

To get the scores themselves is done using the following line of code. 

`model.predict_proba(d_full[['unemp_rate', 'technician_pc']])[:,1]`

## Inverse propensity weighting

[To understand why to use IPW](https://towardsdatascience.com/understanding-inverse-probability-of-treatment-weighting-iptw-in-causal-inference-4e69692bce7e/)

The link above uses a minimal example to explain how, by weighting individual records, IPW balances a dataset. In the example at hand it doubles the number of results in the dataset. By doubling the results, the technique somehow forges results obtained from studies. In the example this forgery problem is handled. After applying the IPW technique, the sex of an individual no longer has influence on its chance to receive the treatment, while on beforehand a female had 75% chance to receive treatment. This gives way to the illustration in which the vertex between sex and treatment is removed.

<img src="https://github.com/user-attachments/assets/c6e72a9d-53d6-46e3-b56e-613b42e2df38" alt="drawing" width="200"/>
<img src="https://github.com/user-attachments/assets/57ae1a48-ebf5-4cc2-9cbe-d2a66c46d1ad" alt="drawing" width="200"/>

### Case study

To test the ideas of IPW ourself, I have applied IPW on [a kaggle dataset](https://www.kaggle.com/datasets/rkiattisak/student-performance-in-mathematics). 

For every student the dataset contains social, gender, racial indicators, some test results and whether or not a test preparation course was followed.

At first data needs to be inspected and prepared, for categorical data dummy binary columns need to be created (IPW is all about numbers).

The social, gender, racial indicators will be used to get an idea of how likely someone is to take the test preparation course. The dependent variable is the result on a math test.

To find out how interesting it would be to take a test preparation course, the Python causallib library was used to calculate a treatment effect.

The propensity scores are calculated using sklearn's LogisticRegression learner. CausalLib IPW model is then used to assign a weight to every record. A higher weight on a student that is in the treated group would indicate only a few students in the treated group are having similar confounders (the social, gender and racial indicators). 

#### Propensity score histogram

Before getting actual results it is interesting to get an idea of the distribution of the students' propensity scores.

![prop_histo](https://github.com/user-attachments/assets/20389ac9-28a3-4c84-bb21-56713a0e7dbd)


From the image above it is to be seen there is a lot of overlap between the group that took the test preparation course and the group that did not. So every type of student that did take the course, has a counterpart that didn't take it. The image also makes clear that the majority of students didn't take the course.

#### Results
The ATE is obtained as can be seen in the code snippet below. The x-cols variable contains all the confounders.

`from causallib.estimation import IPW`

`from sklearn.linear_model import LogisticRegression`

`learner = LogisticRegression()`

`ipw = IPW(learner)`

`x-cols= ['standard', 'group B', 'group C', 'group D', 'group E', "associate's degree", "bachelor's degree", "high school", "master's degree", "some high school", 'female']`

`outcomes = ipw.estimate_population_outcome(data[x_cols], data['test preparation course'], data['math score'])`

`effect = ipw.estimate_effect(outcomes[1], outcomes[0])`

The effect is 4.92, so taking the test preparation course increases the math score by 4.92 points. The maximum score to be obtained for the math test is 100, while on average  one would have a score of 66.03 when not having taken the prep course, while otherwise the score would be 70.95.

#### Assessment

##### Standard mean differences

The weighting has had its effects on the covariates for both the control group and the treated group (left), after weighting there is hardly any difference between them. As I am using crossvalidation, there is a validation fold. This validation fold gives a much more ambiguous impression (right). The dataset only contains data for 1000 students, this could cause these results.

![love](https://github.com/user-attachments/assets/786f5e23-2310-44af-8378-469f85dec081)

##### Propensity score distribution

This graph shows the distribution of propensity scores over the treated and untreated group after weighting. The distribution shows a balanced distribution, which is good. If a given propensity value only has a density only in the treated distribution and not the control (or vice-versa), it is a warning sign that the groups might not be fully comparable to support a causal claim.  Though it might also suggest the model is overfitted. Therefore, it is worth to also examine the plot on a validation set if possible.

![weight_distri](https://github.com/user-attachments/assets/da9efc78-4061-4c11-994d-668527c69097)

##### Receiver-operating characteristic curve

The ROC plots the true positive rate (sensitivity) against the false positive rate (1 - specificity) at various threshold settings. The weighted training ROC shows almost no discriminational power between exposed and control group (which is good). On the contrary, the validation graph shows worse results, the weighted graph should be as close as possible to the chance line and it is not.

![roc](https://github.com/user-attachments/assets/3158b23d-0ddc-4b6f-9e41-9dbf1c226de7)






























