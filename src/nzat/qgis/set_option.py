def set_option(layer_el, name, value):
    option = layer_el.find("Option")
    for child in option:
        if child.get("name") == name:
            child.set("value", value)
            return
    raise RuntimeError(f"missing option {name}")
