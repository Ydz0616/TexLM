# tasks/base.py
from abc import ABC, abstractmethod

class BaseTask(ABC):
    name: str  # e.g. "transpose"

    @abstractmethod
    def build_dsl(self, decomposition: dict, real_matrix):
        """

        According to the input matrix and instruction, 
        generate the DSL

        e.g. "transpose((2, 3, float), (3, 2, float))"
        """
        ...

    @abstractmethod
    def execute(self, dsl_ast, real_matrix):
        """

        Execute the task and return the result matrix/scalor
        
        """
        ...

