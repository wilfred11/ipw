### Propensity Score Matching

The "propensity score" describes how likely a unit is to have been treated, given its covariate values. 
#### Simple case
Suppose for example a simple case where a company builds factories in villages. To naively compare the effects of the factory on village income a simple weighted mean difference between income with and without factory has to be made. This could lead to the conclusion that mean income of a village lowers after building a factory.

![naive](https://github.com/user-attachments/assets/779a2a92-69d3-412c-9985-0b2406054fab)

#### Still a simple case

A better way to compare differences in income for villages with and without factories would be to only compare villages that would be good candidates for building a factory. For this reason the features used to select villages apt for building a factory should be used to find which villages with factories match villages without factories. In this case the unemployment rate and the number of technicians per capita are used to assert whether villages are apt to build a factory near. In this case the matches are made by hand.

![less-naive](https://github.com/user-attachments/assets/f31637ab-e60d-4915-af2e-bece96fd6a72)

#### The propensity score

Using logistic regression one could find one score per individual that sort of like captures all features on which a village is selected, this score makes it possible to match records automatically. 








