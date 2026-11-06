from nzat.qgis.defaults import STYLE


def test_stream_is_not_near_black():
    # Catches stream #00276D, which reads as a black track where a stream runs beside a track.
    assert STYLE["reference_inks"]["stream"] == "#004C99"
