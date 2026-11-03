def fonts_in(style):
    for layer in style["layers"]:
        fonts = layer.get("layout", {}).get("text-font")
        if isinstance(fonts, list):
            for font in fonts:
                if isinstance(font, str):
                    yield layer["id"], font
