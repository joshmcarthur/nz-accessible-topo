from nzat.qgis.qgis_prefix import qgis_prefix


def test_qgis_prefix_uses_the_environment():
    # Catches a Mac run that still points QGIS at /usr.
    assert qgis_prefix(None) == "/usr"
    assert qgis_prefix("") == "/usr"
    assert qgis_prefix("  ") == "/usr"
    assert qgis_prefix("/Applications/QGIS.app/Contents/MacOS") == (
        "/Applications/QGIS.app/Contents/MacOS"
    )
