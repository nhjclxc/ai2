from . import app

def test_test_range():
    min, max = app.get_range_size("bytes=100-1024")
    print(min, max)

def test_tuple_join1():
    req_tpl = (5, 15)
    cache_tpl = (1, 20)
    ret = app.tuple_join( cache_tpl, req_tpl)
    assert ret == (5, 15)

def test_tuple_join2():
    req_tpl = (5, 15)
    cache_tpl = (8, 12)
    ret = app.tuple_join( cache_tpl, req_tpl)
    assert ret == (8, 12)

def test_tuple_join3():
    req_tpl = (5, 15)
    cache_tpl = (2, 12)
    ret = app.tuple_join( cache_tpl, req_tpl)
    assert ret == (5, 12)

def test_tuple_join4():
    req_tpl = (5, 15)
    cache_tpl = (12, 18)
    ret = app.tuple_join( cache_tpl, req_tpl)
    assert ret == (12, 15)

def test_tuple_join5():
    req_tpl = (15, 25)
    cache_tpl = (1, 8)
    ret = app.tuple_join( cache_tpl, req_tpl)
    assert ret == ()

def test_tuple_join6():
    req_tpl = (15, 15)
    cache_tpl = (1, 1)
    ret = app.tuple_join( cache_tpl, req_tpl)
    assert ret == ()



