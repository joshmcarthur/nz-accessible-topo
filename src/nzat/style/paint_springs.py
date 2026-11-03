from nzat.style.spring_colour import spring_colour


def paint_springs(builder, rules):
    hot = spring_colour("hot", rules)
    cold = spring_colour("cold", rules)
    hot_layer = builder.layer("Water-Spring-Hot")
    hot_layer["paint"]["text-color"] = hot
    if "icon-color" in hot_layer["paint"]:
        hot_layer["paint"]["icon-color"] = hot
    builder.note("R-17", "Water-Spring-Hot", f"text → {hot}; icon stays spring_hot_pnt")
    cold_layer = builder.layer("Water-Spring-Cold")
    cold_layer["paint"]["text-color"] = cold
    cold_layer["paint"]["icon-color"] = cold
    builder.note(
        "R-17", "Water-Spring-Cold", f"icon+text → {cold}; icon stays spring_cold_pnt"
    )
