import os
import xml.etree.ElementTree as ET

from nzat.qgis.apply import apply


def main(src, dst):
    doctype = ""
    with open(src, encoding="utf-8") as handle:
        first = handle.readline()
        if first.startswith("<!DOCTYPE"):
            doctype = first if first.endswith("\n") else first + "\n"
    root = ET.parse(src).getroot()
    labels = apply(root, project_dir=os.path.dirname(os.path.abspath(dst)))
    body = ET.tostring(root, encoding="unicode")
    with open(dst, "w", encoding="utf-8") as handle:
        handle.write(doctype)
        handle.write(body)
    print(f"labels {labels}")
    print(f"wrote {dst}")
