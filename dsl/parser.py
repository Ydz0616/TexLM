# dsl/parser.py

def parse_dsl(dsl: str) -> dict:
    """

    A simple parser which supports multiple ops

    Output format:
    {
      "op": "transpose",
      "input": (r, c, "float"),
      "output": (c, r, "float"),
    }
    """
    dsl = dsl.strip()
    if dsl.startswith("transpose"):
        inner = dsl[len("transpose("):-1]
        parts = inner.split("),")
        in_part = parts[0].strip().lstrip("(").strip()
        out_part = parts[1].strip().lstrip("(").rstrip(")").strip()

        def to_tuple(p):
            items = [x.strip() for x in p.split(",")]
            return (int(items[0]), int(items[1]), items[2])

        return {
            "op": "transpose",
            "input": to_tuple(in_part),
            "output": to_tuple(out_part),
        }

    # TODO: branches e.g. matmul, add
    # elif dsl.startswith("matmul"): ...
    # elif dsl.startswith("add"): ...
    else:
        raise ValueError(f"Unknown DSL op: {dsl}")

