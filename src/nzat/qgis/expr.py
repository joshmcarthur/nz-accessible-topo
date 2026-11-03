def expr(props, name):
    node = props.find(f"Option[@name='{name}']")
    if node is None:
        return None
    expression = node.find("Option[@name='expression']")
    return None if expression is None else expression.get("value")
