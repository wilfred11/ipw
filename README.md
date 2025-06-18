### Propensity Score Matching

The "propensity score" describes how likely a unit is to have been treated, given its covariate values. 
#### Simple case
Suppose for example a simple case where a company builds factories in villages. To naively compare the effects of the factory on village income a simple weighted mean difference between income with and without factory has to be made. This could lead to the conclusion that the mean income of a village lowers after building a factory nearby.

![naive](https://github.com/user-attachments/assets/779a2a92-69d3-412c-9985-0b2406054fab)

#### Still a simple case

A better way to compare differences in income for villages with and without factories would be to only compare villages that would be good candidates for building a factory. For this reason the features used to select villages apt for building a factory should be used to find which villages with factories match villages without factories. In this case the unemployment rate and the number of technicians per capita are used to assert whether villages are apt to build a factory near. In this case the matches are made by hand. And the records that have no match are excluded from effect calculations. Average Treatment Effect calculated according to this method is probably a better measure.

![less-naive](https://github.com/user-attachments/assets/191190a7-d5a9-4010-9d9b-dc6f910e5ce6)


#### The propensity score

Using logistic regression one could find one score per individual village. This score, that captures all features on which a village is selected, makes it possible to match records automatically, and is more accurate than handpicking records.

![prop](https://github.com/user-attachments/assets/d987d67b-7e47-4c18-b20c-13991a06f86e)











