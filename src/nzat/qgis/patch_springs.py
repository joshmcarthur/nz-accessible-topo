from nzat.qgis.category_symbol import category_symbol
from nzat.qgis.defaults import STYLE
from nzat.qgis.properties_map import properties_map
from nzat.qgis.put_expr import put_expr
from nzat.qgis.require_field import require_field
from nzat.qgis.rgba import rgb_call


def patch_springs(layer, style=None):
    style = style or STYLE
    hot = style["springs"]["hot"]
    cold = style["springs"]["cold"]
    require_field(layer, "type")
    require_field(layer, "temperature_indicator")
    renderer = layer.find("renderer-v2")
    if renderer.get("attr") == "feature_type":
        renderer.set("attr", "type")
    symbol = category_symbol(layer, "spring")
    marker = symbol.find("layer[@class='SimpleMarker']")
    props = properties_map(marker.find("data_defined_properties"))
    put_expr(
        props,
        "name",
        f"if(\"temperature_indicator\" = 'hot', '{hot['glyph']}', '{cold['glyph']}')",
    )
    put_expr(
        props,
        "fillColor",
        "if(\"temperature_indicator\" = 'hot',"
        f" {rgb_call(hot['colour'])},"
        f" {rgb_call(cold['colour'])})",
    )
