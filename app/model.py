from dataclasses import dataclass
from typing import List, Callable

from app.types.selector import Selector


@dataclass
class ReaperTask:
    name: str
    args: list = []
    kwargs: dict = {}


@dataclass
class ReaperJob:
    name: str
    steps: List[ReaperTask]


@dataclass
class ReaperOptions:
    name: str
    jobs: List[ReaperJob]
    headless: bool = True
    repeat: int = 1
    delay: float = 1


@dataclass
class TargetData:
    name: str
    method: Callable
    selector: Selector
