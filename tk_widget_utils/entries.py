from collections.abc import Callable
from dataclasses import dataclass
import functools as ft
import tkinter as tk
from typing import Literal, TypeVar
from enum import Enum, IntEnum


class _StrEnum(str, Enum):
    """Enum where members are also (and must be) strs"""

    pass


class ActionType(IntEnum):
    INSERT = 1
    DELETE = 0
    FOCUS_OR_FORCE = -1


class TriggerType(_StrEnum):
    FOCUS_IN = "focusin"
    FOCUS_OUT = "focusout"
    FORCED = "forced"
    KEY = "key"


class ValidationType(_StrEnum):
    ALL = "all"
    FOCUS = "focus"
    FOCUS_IN = "focusin"
    FOCUS_OUT = "focusout"
    FORCED = "forced"
    KEY = "key"
    NONE = "none"


@dataclass(frozen=True)
class VcmdParams:
    """Dataclass for tkinter entry validate command params."""

    d: str  # action_type
    i: str  # index
    P: str  # text_allowed_to_edit
    s: str  # text_prior_to_edit
    S: str  # text_being_changed
    v: str  # validation_type
    V: str  # trigger_type
    W: str  # widget_name

    @property
    def action_type(self) -> ActionType:
        """Type of action:
        1 for insert,
        0 for delete,
        or -1 for focus, forced or textvariable validation.
        """
        return ActionType(int(self.d))

    @property
    def index(self) -> int:
        """Index of char string to be inserted/deleted,
        if any, otherwise -1.
        """
        return int(self.i)

    @property
    def text_allowed_to_edit(self) -> str:
        """The value of the entry if the edit is allowed.
        If you are configuring the entry widget to have a new textvariable,
        this will be the value of that textvariable.
        """
        return self.P

    @property
    def text_prior_to_edit(self) -> str:
        """The current value of entry prior to editing."""
        return self.s

    @property
    def text_being_changed(self) -> str:
        """The text string being inserted/deleted,
        if any, empty string otherwise.
        """
        return self.S

    @property
    def validation_type(self) -> ValidationType:
        """The type of validation currently set."""
        return ValidationType(self.v)

    @property
    def trigger_type(self) -> TriggerType:
        """The type of validation that triggered the callback
        (key, focusin, focusout, forced).
        """
        return TriggerType(self.V)

    @property
    def widget_name(self) -> str:
        """The name of the entry widget."""
        return self.W


_TkEntryType = TypeVar("_TkEntryType", bound=tk.Entry)


def set_vcmd(
    widget: _TkEntryType,
    func: Callable[[_TkEntryType, VcmdParams], bool],
    type_: Literal[
        "none", "focus", "focusin", "focusout", "key", "all"
    ] = ValidationType.ALL.value,
) -> _TkEntryType:
    """Configures validate command to entry widget.

    Returns widget that validate command configured.
    """

    @ft.wraps(func)
    def _func(d, i, P, s, S, v, V, W) -> bool:
        return func(widget, VcmdParams(d, i, P, s, S, v, V, W))

    vcmd = (widget.register(_func), *(f"%{a}" for a in "diPsSvVW"))
    widget.configure(validate=type_, vcmd=vcmd)
    return widget
