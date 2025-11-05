# dsl/grammar.py
DSL_GRAMMAR = r"""
// ---------- Terminals ----------
LBRACK: "["
RBRACK: "]"
LPAR: "("
RPAR: ")"
COMMA: ","
SP: " "

NUMBER: /[-+]?(?:\d+(?:\.\d+)?|\.\d+)/

// ---------- Rules ----------
start: call | matrix

call: fname LPAR start RPAR
    | "multiply" LPAR start COMMA SP start RPAR
    | "add"      LPAR start COMMA SP start RPAR

fname: "transpose" | "inverse"

// Matrix literal: [[1,2],[3,4]]
matrix: LBRACK rows RBRACK
rows: row (COMMA SP row)*
row: LBRACK elements RBRACK
elements: NUMBER (COMMA SP NUMBER)*
"""
