DSL_GRAMMAR = """
start: transpose(start)
        | inverse(start)
        | multiply(start, start)
        | add(start, start)
        | "[" MATRIX "]"

MATRIX: "[" ROW "]"
        | "[" ROW "]" "," MATRIX

ROW: ELEMENT 
    | ELEMENT "," ROW

ELEMENT: ^[-+]?(?:\d+\.?\d*|\.\d+)$
"""