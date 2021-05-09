import pytest

from .. import checkers as chk


class Test_IsEmpty:
    def test_returns_true(self):
        assert chk.is_empty("")

    @pytest.mark.parametrize("v", ("a", "foo", "1", "3.14"))
    def test_returns_false(self, v):
        assert not chk.is_empty(v)


class Test_IsInt:
    @pytest.mark.parametrize("v", ("1", "56", "79822", "0", "-0", "-86"))
    def test_returns_true(self, v):
        assert chk.is_int(v)

    @pytest.mark.parametrize("v", ("a", "foo", "1.", "--0.5", "-"))
    def test_returns_false(self, v):
        assert not chk.is_int(v)


class Test_ByteLen:
    @pytest.mark.parametrize(
        "v, len_",
        (("あ", 2), ("받", 2), ("汉", 2), ("转注字", 6), ("hoge", 4), ("foo", 3)),
    )
    def test_returns_len(self, v, len_):
        assert chk.get_bytelen(v) == len_
