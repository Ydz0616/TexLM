# tasks/transpose.py
from tasks.base import BaseTask
from dsl.parser import parse_dsl
from dsl.executor import execute_transpose

class TransposeTask(BaseTask):
    name = "transpose"

    def build_dsl(self, decomposition: dict, real_matrix):
        rows = len(real_matrix)
        cols = len(real_matrix[0]) if real_matrix else 0
        # 这里也可以让 LLM 来，但其实转置这类是可计算的，没必要问 LLM
        return f"transpose(({rows}, {cols}, float), ({cols}, {rows}, float))"

    def execute(self, dsl_ast, real_matrix):
        # 这里我们知道是 transpose，直接调对应的 executor
        return execute_transpose(dsl_ast, real_matrix)
