from myDates import *



def test_valid_date_true():
    assert valid_date('01/07/2000', dt_format = "%d/%m/%Y") == True
    assert valid_date('1/07/2000',dt_format = "%d/%m/%Y") == True
    assert valid_date('01/7/2000', dt_format = "%d/%m/%Y") == True
    assert valid_date('01/07/1900', dt_format = "%m/%d/%Y") == True
    assert valid_date('31/01/2032', dt_format = "%d/%m/%Y") == True
    assert valid_date('31/01/2032 ', remove_whitespace=True) == True


def test_valid_date_false():
    assert valid_date('01/07/20') == False
    assert valid_date('01-07/2022') == False
    assert valid_date('0107/2022') == False
    assert valid_date('01-07-2022') == False
    assert valid_date('01/ 07/2022') == False
    assert valid_date('01/ 07/2022 ', remove_whitespace=False) == False
    assert valid_date('31/01/2032', dt_format = "%m/%d/%Y") == False







