import xml.etree.ElementTree as ET


def put_expr(props, name, expression):
    for child in list(props):
        if child.get("name") == name:
            props.remove(child)
    node = ET.Element("Option", {"name": name, "type": "Map"})
    ET.SubElement(node, "Option", {"name": "active", "type": "bool", "value": "true"})
    ET.SubElement(
        node, "Option", {"name": "expression", "type": "QString", "value": expression}
    )
    ET.SubElement(node, "Option", {"name": "type", "type": "int", "value": "3"})
    props.append(node)
