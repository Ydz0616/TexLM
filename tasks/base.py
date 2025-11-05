# tasks/base.py
from abc import ABC, abstractmethod

class BaseTask(ABC):
    name: str  # e.g. "transpose"

    @abstractmethod
    def execute(self, dsl_ast, real_matrix):
        """

        Execute the task and return the result matrix/scalor
        
        """
        ...

