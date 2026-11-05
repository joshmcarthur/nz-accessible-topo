from nzat.qgis.is_spot_height import is_spot_height


def test_spot_heights_are_numbers_with_an_optional_m():
    # Catches a height left movable by the fit (log 0077), or a name such as
    # "A57J" or "Sch" pinned as a height.
    assert is_spot_height("445")
    assert is_spot_height("298m")
    assert is_spot_height(" 35m ")
    assert not is_spot_height("A57J")
    assert not is_spot_height("Sch")
    assert not is_spot_height("Mt Cavendish")
    assert not is_spot_height(None)
