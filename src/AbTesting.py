import numpy as np
import pandas as pd
from statsmodels.stats.proportion import proportion_confint
import scipy.stats as st
from time import time
import seaborn as sns
from matplotlib import pyplot as plt


def elapsed_time(func):
    def wrapper(*args, **kwargs):
        start = time()

        func(*args, **kwargs)

        end = time()

        print(f"Execution time of the function {func.__name__} is {(end - start):.4f}s")

    return wrapper


class AbTesting:
    __slots__ = ('data', 'variant_col', 'target_col', 'summary_data')

    def __init__(self, data: pd.DataFrame(), variant_col: str = "VARIANT_NAME", target_col: str = "REVENUE"):

        self.data = data
        self.variant_col = variant_col
        self.target_col = target_col

        self.summary_data = self.describe_data()

    def describe_data(self):

        return self.data.groupby(by=self.variant_col)[self.target_col].describe()

    def sanity_check(self, alpha=0.05):

        ab_user_count = tuple(self.summary_data["count"])

        conf_int = proportion_confint(sum(ab_user_count) / 2, sum(ab_user_count), alpha=alpha, method='normal')

        check_result = "Sanity Check Pass" if ((min(ab_user_count) > min(conf_int) * sum(ab_user_count)) & (
                    max(ab_user_count) < max(conf_int) * sum(ab_user_count))) else "Sanity Check Fail"

        print(
            f"%{(1 - alpha) * 100} Confidence Interval for phat to be considered as random division of control/variant is : {tuple(round(x, 4) for x in conf_int)}" + "\n"

                                                                                                                                                                      "Your sanity check result is : ",
            check_result)

    def simulation(self, iter_count=10000):

        simulation_result = []

        # split_count_1,split_count_2 = (self.summary_data["count"].min()//2,self.summary_data["count"].max()//2)

        split_count_1 = self.summary_data["count"].min() // 2

        for i in range(iter_count):
            data_control = self.data[self.data[self.variant_col] == "control"].sample(frac=1).reset_index(drop=True)
            data_variant = self.data[self.data[self.variant_col] == "variant"].sample(frac=1).reset_index(drop=True)

            first_part = (data_variant.loc[:split_count_1, self.target_col].sum() + data_control.loc[:split_count_1,
                                                                                    self.target_col].sum()) / (
                                     split_count_1 * 2)
            second_part = (data_variant.loc[split_count_1:, self.target_col].sum() + data_control.loc[split_count_1:,
                                                                                     self.target_col].sum()) / (
                              self.summary_data["count"].max())

            simulation_result.append(second_part - first_part)

        return simulation_result

    def min_samples_per_group(self, alpha=0.05, power=0.8, two_tailed=True):

        pop_std = self.statistical_calculations()[1]

        if two_tailed:
            min_samples_per_group = 2 * ((st.norm.ppf((1 - alpha / 2)) + st.norm.ppf(power)) ** 2) * (pop_std ** 2) / (
                        np.diff(self.related_data["mean"])[0] ** 2)
        else:
            min_samples_per_group = 2 * ((st.norm.ppf((1 - alpha)) + st.norm.ppf(power)) ** 2) * (pop_std ** 2) / (
                        np.diff(self.related_data["mean"])[0] ** 2)

        return min_samples_per_group

    def visualization(self, conf_simulation, conf_int, alpha, two_tailed):

        mean_diff = (self.related_data.loc[self.related_data[self.variant_col] == "variant", "mean"].values -
                     self.related_data.loc[self.related_data[self.variant_col] == "control", "mean"].values)

        size = int(np.mean(self.summary_data["count"]))

        SE = self.statistical_calculations()[0]

        fig, axs = plt.subplots(ncols=2, figsize=(18, 8))

        sns.kdeplot(conf_simulation, ax=axs[0]).set(title="Simulation of Shuffling Result")

        sns.kdeplot(np.random.normal(loc=0, scale=SE, size=int(self.related_data["count"].max())), ax=axs[1]).set(title="Central Limit Theorem")

        if two_tailed:

            axs[0].axvline(np.percentile(conf_simulation, (alpha / 2) * 100), color="red",
                           label="%" + str((alpha / 2) * 100))
            axs[0].axvline(np.percentile(conf_simulation, (1 - alpha / 2) * 100), color="green",
                           label="%" + str((1 - alpha / 2) * 100))
            axs[0].axvline(mean_diff, color="black", label=str("test_mean_diff"), ls=":")
            axs[0].legend()

            axs[1].axvline(conf_int[1], color="green", label="%" + str((1 - alpha / 2) * 100))
            axs[1].axvline(conf_int[0], color="red", label="%" + str((alpha / 2) * 100))
            axs[1].axvline(mean_diff, color="black", label=str("test_mean_diff"), ls=":")
            axs[1].legend()

        else:

            axs[0].axvline(np.percentile(conf_simulation, (1 - alpha) * 100), color="green",
                           label="%" + str((1 - alpha) * 100))
            axs[0].axvline(mean_diff, color="black", label=str("test_mean_diff"), ls=":")
            axs[0].legend()
            axs[1].axvline(conf_int[0], color="green", label="%" + str((1 - alpha) * 100))
            axs[1].axvline(mean_diff, color="black", label=str("test_mean_diff"), ls=":")
            axs[1].legend()

        plt.plot()
