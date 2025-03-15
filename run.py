import logging
import os
import argparse
from conf import pytest_addoption


# 解析命令行参数
def parse_args():
    parser = argparse.ArgumentParser("run automated testcases")
    parser.add_argument(
        "--env",
        default="stage",
        choices=["stage", "prod"],
        help="environment to run testcases"
    )


def set_env_vars(env):
    os.environ["ENV"] = env


if __name__ == "__main__":
    args = parse_args()
    set_env_vars(args.env)
