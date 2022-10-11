from operator import methodcaller
from typing import Any, List, Dict

import yaml
from yaml.loader import Loader

from driver import DefaultWebDriver
from spider import SeleniumSpider
from selector import *


yaml_mapper = {}


def parse_yaml(filepath: str):
    with open(filepath) as file:
        options = yaml.load(file, Loader)
    return options


def run_task():
    ...


def run_steps(
    actor, 
    repeat: int,
    steps: List[Dict[str, Any]],
    task_key_name: str = "name",
    task_key_args: str = "args",
    task_key_kwargs: str = "kwargs"
    ):
        for iter_ in range(repeat):
            for task in steps:
                methodcaller(
                    task.get(task_key_name), 
                    *task.get(task_key_args),
                    **task.get(task_key_kwargs)
                )


def run_jobs():
    for i in range(2):
        ...

options = parse_yaml("sample/scripts/tokopedia.yaml")

# driver = DefaultWebDriver().create_driver()


