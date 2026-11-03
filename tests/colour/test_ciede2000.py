from nzat.colour.ciede2000 import ciede2000


def test_ciede2000_reference():
    # Sharma, Wu & Dalal (2005) test pairs 1 and 3
    assert round(ciede2000((50, 2.6772, -79.7751), (50, 0, -82.7485)), 4) == 2.0425
    assert round(ciede2000((50, -1.1848, -84.8006), (50, 0, -82.7485)), 4) == 1.0
