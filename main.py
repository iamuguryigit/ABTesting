from src.ABTesting_Continuous import AbTesting_Continuous
from src.ABTesting_Binary import AbTesting_Binary
from src.preprocess import preprocess_binary,preprocess_continuous
from src.config import retention_data_path,revenue_data_path

def run_ab_binary_test(variant_col:str,target_col:str,two_tailed:bool=True,alpha=0.05,power=0.8,iter_count=10000):

    retention_ab_data = preprocess_binary(retention_data_path)

    retention_ab = AbTesting_Binary(data = retention_ab_data,variant_col = variant_col,target_col = target_col)

    retention_ab.ab_conf_interval(two_tailed=two_tailed, alpha=alpha, power=power, iter_count=iter_count)


def run_ab_cont_test(variant_col: str, target_col: str, two_tailed: bool = True, alpha=0.05, power=0.8,iter_count=10000):

    revenue_ab_data = preprocess_continuous(revenue_data_path)

    revenue_ab = AbTesting_Continuous(data=revenue_ab_data, variant_col=variant_col, target_col=target_col)

    revenue_ab.ab_conf_interval(two_tailed=two_tailed, alpha=alpha, power=power, iter_count=iter_count)


if __name__ == '__main__':

    print("AB RESULT FOR RETENTION TEST")
    run_ab_binary_test(variant_col="version",target_col = "retention_7",two_tailed = True,alpha = 0.05,power = 0.8,iter_count = 1000)

    print()

    print("AB RESULT FOR REVENUE TEST")

    run_ab_cont_test(variant_col="VARIANT_NAME", target_col="REVENUE", two_tailed=True, alpha=0.05, power=0.8,iter_count=1000)



