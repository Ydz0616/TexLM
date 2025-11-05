# tasks/transpose.py
from tasks.base import BaseTask
from dsl.executor import execute_transpose

class TransposeTask(BaseTask):
    name = "transpose"

    def execute(self, dsl_ast, real_matrix):

        return execute_transpose(dsl_ast, real_matrix)
