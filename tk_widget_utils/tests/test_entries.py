import tkinter as tk
from unittest.mock import MagicMock

import pytest

from ..entries import (
    VcmdParams,
    ActionType,
    ValidationType,
    TriggerType,
    set_vcmd,
)


@pytest.fixture
def vparams_kwargs() -> dict[str, str]:
    return {a: "" for a in "diPsSvVW"}


class Test_VcmdParams:
    class Test_ActionType:
        @pytest.mark.parametrize(
            "arg, type_, val",
            (
                ("0", ActionType.DELETE, 0),
                ("1", ActionType.INSERT, 1),
                ("-1", ActionType.FOCUS_OR_FORCE, -1),
            ),
        )
        def test_returns_action_type(self, vparams_kwargs, arg, type_, val):
            vparams_kwargs["d"] = arg
            v = VcmdParams(**vparams_kwargs)
            assert v.action_type is type_ == val

    class Test_Index:
        @pytest.mark.parametrize("arg, val", (("0", 0), ("1", 1), ("-1", -1)))
        def test_returns_index(self, vparams_kwargs, arg, val):
            vparams_kwargs["i"] = arg
            v = VcmdParams(**vparams_kwargs)
            assert v.index == val

    class Test_TextAllowedToEdit:
        @pytest.mark.parametrize("arg, val", (("a", "a"), ("", "")))
        def test_returns_text_if_the_edit_is_allowed(
            self, vparams_kwargs, arg, val
        ):
            vparams_kwargs["P"] = arg
            v = VcmdParams(**vparams_kwargs)
            assert v.text_allowed_to_edit == val

    class Test_TextPriorToEdit:
        @pytest.mark.parametrize("arg, val", (("a", "a"), ("", "")))
        def test_returns_text_prior_to_edit(self, vparams_kwargs, arg, val):
            vparams_kwargs["s"] = arg
            v = VcmdParams(**vparams_kwargs)
            assert v.text_prior_to_edit == val

    class Test_TextBeingChanged:
        @pytest.mark.parametrize("arg, val", (("a", "a"), ("", "")))
        def test_returns_being_inserted_or_deleted(
            self, vparams_kwargs, arg, val
        ):
            vparams_kwargs["S"] = arg
            v = VcmdParams(**vparams_kwargs)
            assert v.text_being_changed == val

    class Test_ValidationType:
        @pytest.mark.parametrize(
            "arg, type_, val",
            (
                ("all", ValidationType.ALL, "all"),
                ("focus", ValidationType.FOCUS, "focus"),
                ("focusin", ValidationType.FOCUS_IN, "focusin"),
                ("focusout", ValidationType.FOCUS_OUT, "focusout"),
                ("forced", ValidationType.FORCED, "forced"),
                ("key", ValidationType.KEY, "key"),
                ("none", ValidationType.NONE, "none"),
            ),
        )
        def test_returns_type_that_currently_set(
            self, vparams_kwargs, arg, type_, val
        ):
            vparams_kwargs["v"] = arg
            v = VcmdParams(**vparams_kwargs)
            assert v.validation_type is type_ == val

    class Test_TriggerType:
        @pytest.mark.parametrize(
            "arg, type_, val",
            (
                ("focusin", TriggerType.FOCUS_IN, "focusin"),
                ("focusout", TriggerType.FOCUS_OUT, "focusout"),
                ("forced", TriggerType.FORCED, "forced"),
                ("key", TriggerType.KEY, "key"),
            ),
        )
        def test_returns_type_that_triggered_the_callback(
            self, vparams_kwargs, arg, type_, val
        ):
            vparams_kwargs["V"] = arg
            v = VcmdParams(**vparams_kwargs)
            assert v.trigger_type is type_ == val

    class Test_WidgetName:
        def test_returns_widget_name(self, vparams_kwargs):
            vparams_kwargs["W"] = ".!entry"
            v = VcmdParams(**vparams_kwargs)
            assert v.widget_name == ".!entry"


class Test_SetVcmd:
    def setup_method(self, method):
        self.root = tk.Tk()
        self.strvar = tk.StringVar()
        self.ent = tk.Entry(self.root, textvariable=self.strvar)
        self.sub_ent = tk.Entry(self.root)
        self.ent.pack()
        self.sub_ent.pack()

    def teardown_method(self, method):
        self.root.destroy()

    def test_allows_to_edit_if_func_returns_true(self, mocker):
        func: MagicMock = mocker.MagicMock(return_value=True)
        self.strvar.set("a")
        assert set_vcmd(self.ent, func) is self.ent
        self.strvar.set("b")
        assert self.ent.get() == "b"
        vp = VcmdParams(
            "-1", "-1", "b", "a", "", "all", "forced", str(self.ent)
        )
        func.assert_called_once_with(self.ent, vp)

    def test_not_allows_to_edit_if_func_returns_false(self, mocker):
        func: MagicMock = mocker.MagicMock(return_value=False)
        self.strvar.set("a")
        assert set_vcmd(self.ent, func) is self.ent
        self.ent.insert(0, "b")
        assert self.ent.get() == "a"
        vp = VcmdParams("1", "0", "ba", "a", "b", "all", "key", str(self.ent))
        func.assert_called_once_with(self.ent, vp)

    def test_allows_to_edit_if_validate_type_not_matches_trigger_type(
        self, mocker
    ):
        func: MagicMock = mocker.MagicMock(return_value=False)
        self.strvar.set("a")
        assert set_vcmd(self.ent, func, ValidationType.KEY.value) is self.ent
        self.strvar.set("b")
        assert self.ent.get() == "b"
        vp = VcmdParams(
            "-1", "-1", "b", "a", "", "key", "forced", str(self.ent)
        )
        func.assert_called_once_with(self.ent, vp)

    def test_allows_to_edit_and_not_calls_func_if_validate_type_is_none(
        self, mocker
    ):
        func: MagicMock = mocker.MagicMock(return_value=False)
        self.strvar.set("a")
        assert set_vcmd(self.ent, func, ValidationType.NONE.value) is self.ent
        self.ent.insert(0, "b")
        assert self.ent.get() == "ba"
        self.strvar.set("foo")
        assert self.ent.get() == "foo"
        func.assert_not_called()
