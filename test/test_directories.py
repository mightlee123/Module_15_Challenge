import os

def test_AGG_path():
    assert os.path.isfile("../src/Resources/AGG.csv") == True

def test_BTC_path():
    assert os.path.isfile("../src/Resources/BTC.csv") == True

def test_SPY_path():
    assert os.path.isfile("../src/Resources/SPY.csv") == True