from src.AbTesting import AbTesting,elapsed_time
import numpy as np
import pandas as pd
import scipy.stats as st


class AbTesting_Continuous(AbTesting):

    def __init__(self, data: pd.DataFrame(), variant_col: str = "VARIANT_NAME", target_col: str = "REVENUE"):

        super().__init__(data, variant_col, target_col)

        self.related_data = self.summary_data[["mean", "count", "std"]].reset_index()

    def statistical_calculations(self):

        SE = np.sqrt(sum((self.related_data["std"] ** 2) / (self.related_data["count"])))

        pop_std = np.sqrt(
            sum((self.related_data["std"] ** 2) * (self.related_data["count"])) / sum(self.related_data["count"]))

        cohen = (self.related_data.loc[self.related_data[self.variant_col] == "variant", "mean"].values -
                 self.related_data.loc[self.related_data[self.variant_col] == "control", "mean"].values)[0] / pop_std

        return SE, pop_std, cohen

    @elapsed_time
    def ab_conf_interval(self, alpha=0.05, two_tailed=False, power=0.8, iter_count=10000):

        sanity_check = self.sanity_check(alpha=alpha)

        SE, pop_std, cohen = self.statistical_calculations()

        conf_int = (st.norm.ppf(alpha / 2) * SE, 0 + st.norm.ppf(1 - alpha / 2) * SE) if two_tailed else (
        0 + st.norm.ppf(1 - alpha) * SE,)

        min_samples_per_group = self.min_samples_per_group(alpha=alpha, power=power, two_tailed=two_tailed)

        conf_simulation = self.simulation(iter_count=iter_count, two_tailed=two_tailed)

        simulation_interval = ((np.percentile(conf_simulation, alpha * 100 / 2),
                                np.percentile(conf_simulation, (1 - alpha / 2) * 100))) if two_tailed else (
        (np.percentile(conf_simulation, (1 - alpha) * 100),))

        print(f"Min samples required per group for %{power * 100} power is: ", round(min_samples_per_group, 0), "\n" +

              "SE unpooled is : ", round(SE, 4), "\n" + "Hypothetical confidence interval is :",
              tuple(round(x, 4) for x in conf_int), "\n" +

              "SE of simulation is : ", round(np.std(conf_simulation), 4), "\n" +

              "Confidence interval of simulation is :", tuple(round(x, 4) for x in simulation_interval))

        mean_diff = (self.related_data.loc[self.related_data[self.variant_col] == "variant", "mean"].values -
                     self.related_data.loc[self.related_data[self.variant_col] == "control", "mean"].values)

        if two_tailed:

            if (mean_diff < conf_int[0]) | (mean_diff > conf_int[1]):

                print("Reject H0 --> There is a statistically significant result!")

            else:

                print("Fail to reject H0 -->There is not a statistically significant result!")


        else:

            if mean_diff > conf_int[0]:

                print("Reject H0 --> There is a statistically significant result!")


            else:

                print("Fail to reject H0 -->There is not a statistically significant result!")

        print("Cohen's d is : ", cohen)

        self.visualization(conf_simulation=conf_simulation, conf_int=conf_int, alpha=alpha, two_tailed=two_tailed)


