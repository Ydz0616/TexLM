# dsl/executor.py

def execute_transpose(ast_dsl: dict, matrix):
    # we could also check shape here
    return [list(row) for row in zip(*matrix)]

def execute_matmul(ast_dsl: dict, matrix_a):
    # just a place holder
    raise NotImplementedError("matmul executor not implemented yet")
