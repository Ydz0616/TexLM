import ast
import numpy as np

def evaluate(ast_object : ast.Module) -> np.ndarray:
    assert isinstance(ast_object, ast.Module), "Trying to evaulate something that is not an ast module"
    assert len(ast_object.body) == 1, "There is more than one body in the ast module"
    np_matrix = visit_node(ast_object.body[0].value)
    return np_matrix
    # TODO: convert np objects back to regular lists, int, and floats

def visit_node(node) -> np.ndarray:
    match node:
        case ast.Call():  # a matrix operation
            return visit_call(node)
        case ast.List():  # a matrix
            return visit_list(node)
        case _:
            assert False, f"Unrecognized ast node: {node}"


def visit_list_helper(element):
    match element:
        case ast.Constant():
            return element.value
        case ast.List():
            return [visit_list_helper(e) for e in element.elts]
        case _:
            assert False, f"Unrecognized member of list: {element}"

def visit_list(node : ast.List) -> np.ndarray:
    list = visit_list_helper(node)
    return np.array(list)

def visit_call(node : ast.Call) -> np.ndarray:
    match node.func.id:
        case "transpose":
            return transpose(node)
        case "inverse":
            return inverse(node)
        case "add":
            return add(node)
        case "multiply":
            return multiply(node)
        case _:
            assert False, f"Unrecognized matrix operation: {node.func.id}"


# Operations

def transpose(node : ast.Call) -> np.ndarray:
    assert len(node.args) == 1, "A transpose operation was not given one argument"
    matrix = visit_node(node.args[0])
    matrix_transpose = np.transpose(matrix)
    return matrix_transpose

def inverse(node : ast.Call) -> np.ndarray:
    assert len(node.args) == 1, "An inverse operation was not given one argument"
    matrix = visit_node(node.args[0])
    matrix_inverse = np.linalg.inv(matrix)
    return matrix_inverse

def add(node : ast.Call) -> np.ndarray:
    assert len(node.args) == 2, "An add operation was not given two arguments"
    a = visit_node(node.args[0])
    b = visit_node(node.args[1])
    sum = a + b
    return sum

def multiply(node : ast.Call) -> np.ndarray:
    assert len(node.args) == 2, "An multiply operation was not given two arguments"
    a = visit_node(node.args[0])
    b = visit_node(node.args[1])
    product = a @ b
    return product