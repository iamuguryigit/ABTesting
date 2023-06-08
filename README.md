# Analysis of an AB Test

This project aims to provide a guide to understanding, optimizing and evaluating A/B tests. 

_In order to obtain meaningful results from an A/B test, we utilize a concept called the **Central Limit Theorem**. This theorem tells us that when we collect a large enough sample size, the distribution of our data tends to follow a predictable pattern, even if the underlying data itself is not normally distributed._

There will be two parts including continuous (revenue) and binary (retention) targets. We will be using revenue data from : https://www.kaggle.com/datasets/sergylog/ab-test-data
and retention data from : https://www.kaggle.com/datasets/arpitdw/cokie-cats. 

# Continuous (Revenue) Data

Sample preview of the revenue data:

![Revenue data](ab_images/continuous/head.png)

Create an instance of an AbTesting_Continous class. Variant col is used to describe the column showing AB groups and target col is used for targeted data. Summary_data is an attribute of the instance showing to describe the data. 

![Revenue data](ab_images/continuous/summarydata.png)

Sanity check is a method created in an inherited AbTesting class. By using it you can check whether your division into control and variant groups is random or not. If it is not random, then you should check your experiment and fix it.

![Revenue data](ab_images/continuous/sanity_check.png)

Minimum required sample is a method created in an inherited AbTesting class. By choosing two_tailed, power and alpha parameters you get the minimum required samples per group.

![Revenue data](ab_images/continuous/min_samples_per_group.png)

statistical_calculations is a method created in AbTesting_Continuous class. It returns a tuple and the first element is showing the unpooled sampling error and the second one is the population standard deviation which is calculated by the sample standard deviations and the last one is cohen's d number to see the effect size.

![Revenue data](ab_images/continuous/statistical_calculations.png)

Simulation is a method created in an inherited AbTesting class. The only parameter is iteration counts and basically, it shuffles the data between ab groups and calculate the mean differences. Iteration count determines the count of this operation.

![Revenue data](ab_images/continuous/cont_simulation.png)

This is the main function. ab_conf_interval is a method created in AbTesting_Continuous class. Alpha is the first parameter showing the maximum limit you allow for the probability that your results are due to chance. two_tailed parameter is showing whether the difference between groups are important for both ways or in just one way. power is a parameter used to call the min_samples_per_group function. iter_count is used to call the simulation function. This method is calling all the functions and showing a comprehensive result for your test. It also contains two graphs, the first one is showing the result of shuffling and the second one is the result using central limit theorem.

![Revenue data](ab_images/continuous/ab_conf_interval.png)

# Binary (Retention) Data

All the things for AbTesting_Binary class is almost same with AbTesting_Continuous class. There is no cohens' d calculation and the rest is same except calculations. Therefore, please take a look at the project and contact me if needed.

![Revenue data](ab_images/continuous/binaryresult.jpg)

Feel free to explore the repository, contribute to ongoing projects, and share your feedback. 
