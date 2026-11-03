def category_symbol(layer, value):
    renderer = layer.find("renderer-v2")
    symbol_name = None
    for category in renderer.findall("categories/category"):
        if category.get("value") == value:
            symbol_name = category.get("symbol")
            break
    if symbol_name is None:
        raise RuntimeError(f"no category {value!r} on {layer.findtext('layername')}")
    for symbol in renderer.findall("symbols/symbol"):
        if symbol.get("name") == symbol_name:
            return symbol
    raise RuntimeError(f"no symbol {symbol_name}")
