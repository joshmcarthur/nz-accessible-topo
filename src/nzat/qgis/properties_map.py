import xml.etree.ElementTree as ET


def properties_map(dd_parent):
    option = dd_parent.find("Option")
    if option is None:
        return None
    props = None
    for child in list(option):
        if child.get("name") == "properties":
            props = child
            break
    if props is not None and props.get("type") == "Map":
        return props
    new = ET.Element("Option", {"name": "properties", "type": "Map"})
    if props is not None:
        index = list(option).index(props)
        option.remove(props)
        option.insert(index, new)
    else:
        option.insert(0, new)
    return new
