import xml.etree.ElementTree as ET

from nzat.qgis.patch_draw_order import patch_draw_order


def test_building_point_sits_above_building_fill():
    # Catches church/hut markers left under building polygons.
    root = ET.fromstring(
        """
        <qgis>
          <layer-tree-group>
            <layer-tree-group name="Structure map">
              <layer-tree-layer name="structure_point map"/>
              <layer-tree-layer name="building map"/>
              <layer-tree-layer name="building_point map"/>
            </layer-tree-group>
            <layer-tree-group name="Water">
              <layer-tree-layer name="water_point"/>
            </layer-tree-group>
            <layer-tree-layer name="contour"/>
            <layer-tree-layer name="vegetation map"/>
          </layer-tree-group>
        </qgis>
        """
    )
    patch_draw_order(root)
    structure = root.find("layer-tree-group/layer-tree-group[@name='Structure map']")
    names = [
        child.get("name")
        for child in list(structure)
        if child.tag == "layer-tree-layer"
    ]
    assert names.index("structure_point map") < names.index("building_point map")
    assert names.index("building_point map") < names.index("building map")
    assert root.find("layer-tree-group/layer-tree-group[@name='Water']") is not None
    raised = [
        child.get("name")
        for child in list(structure)
        if child.tag == "layer-tree-layer"
    ]
    assert "water_point" in raised
    assert names.index("building_point map") < raised.index("water_point")
