def require_field(layer, field_name):
    names = [field.get("name") for field in layer.findall("fieldConfiguration/field")]
    if field_name not in names:
        raise RuntimeError(f"{layer.findtext('layername')} has no field {field_name}")
