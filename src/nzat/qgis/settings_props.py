def settings_props(settings):
    dd = settings.find("dd_properties")
    if dd is None:
        return None
    option = dd.find("Option")
    if option is None:
        return None
    props = option.find("Option[@name='properties']")
    if props is None or props.get("type") != "Map":
        return None
    return props
