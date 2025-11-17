import numpy as np
from decimal import Decimal
from typing import Callable

def generate_constraint(m : np.ndarray) -> str:
    assert 1 <= len(m.shape), f"Matrix has too few dimensions: {len(m.shape)}"
    assert 2 >= len(m.shape), f"Matrix has too many dimensions: {len(m.shape)}"

    # TODO: make this depend on the width of the matrix in order to prevent page overflows
    num_sigfigs = 5
    def format_number(n : float | int) -> str:
        if len(str(n).replace('.', '')) <= num_sigfigs:
            return str(n)
        # source: https://stackoverflow.com/questions/6913532/display-a-decimal-in-scientific-notation
        return f'%.{num_sigfigs}e' % Decimal(str(n))

    constraint = "\\begin{bmatrix}\n"

    match len(m.shape):
        case 1:
            constraint += one_dim_constraint(m, format_number)
        case 2:
            constraint += two_dim_constraint(m, format_number)
        case _:
            assert False, f"Matrix has invalid dimensions: {m.shape}"

    constraint += "\\end{bmatrix}"

    return constraint



def one_dim_constraint(m : np.ndarray, fn : Callable[[float | int], str]) -> str:
    constraint = f"{fn(m[0])} "

    for i in range(1, m.shape[0]):
        constraint += f"& {fn(m[i])}"

    return constraint

def two_dim_constraint(m : np.ndarray, fn : Callable[[float | int], str]) -> str:

    constraint = one_dim_constraint(m[0, :], fn)

    for i in range(1, m.shape[0]):
        constraint += "\\ \n" + one_dim_constraint(m[i, :], fn)
    
    return constraint
