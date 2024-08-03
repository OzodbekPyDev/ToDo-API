from dataclasses import dataclass


@dataclass
class UpdateTaskSchema:
    name: str
    description: str
