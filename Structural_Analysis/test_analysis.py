import analysis
import pytest
from math import isclose

def test_flexural_cri():

    moment = analysis.flexural_cri(300, 9.05e6, 77.5)
    assert isclose(moment, 35.032258, abs_tol=0.1)

def test_shear_cri():
    
    shear = analysis.shear_cri(300, 136, 6)
    assert isclose(shear, 146.880, abs_tol=0.1)

def test_ver_defl():
    assert analysis.ver_defl(5000) == 20

def test_laterl_dri():
    assert analysis.laterl_dri(3000) == 20
