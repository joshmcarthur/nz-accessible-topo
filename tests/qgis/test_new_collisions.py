from nzat.qgis.new_collisions import new_collisions


def test_new_collisions_skip_stock_pairs_and_small_overlaps():
    # Catches a stock collision counted as a regression, or a part of one
    # name that overlaps another part of the same name.
    stock = [{"a": "MAIN ROAD", "b": "Sch", "area": 3000}]
    accessible = [
        {"a": "Sch", "b": "MAIN ROAD", "area": 4000},
        {"a": "Witch Hill", "b": "Te Ahi", "area": 2500},
        {"a": "Te Ahi", "b": "Te Ahi", "area": 9000},
        {"a": "445", "b": "Mt Cavendish", "area": 600},
        {"a": "Cass Bay", "b": "177", "area": 8000},
    ]
    found = new_collisions(accessible, stock, 2000)
    assert [(pair["a"], pair["b"]) for pair in found] == [
        ("Cass Bay", "177"),
        ("Witch Hill", "Te Ahi"),
    ]
