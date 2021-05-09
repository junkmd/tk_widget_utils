import tkinter as tk

from tk_widget_utils import entries as wue
from tk_widget_utils import checkers as chk


def validate_int(w: tk.Entry, vp: wue.VcmdParams) -> bool:
    return chk.is_int(vp.text_allowed_to_edit)


def validate_five_or_less_bytelen(w: tk.Entry, vp: wue.VcmdParams) -> bool:
    return chk.get_bytelen(vp.text_allowed_to_edit) <= 5


def main():
    root = tk.Tk()
    tk.Label(master=root, text="int").grid(column=0, row=0)
    int_ent = tk.Entry(master=root, justify=tk.RIGHT)
    int_ent.insert(tk.END, "0")
    wue.set_vcmd(int_ent, validate_int)
    int_ent.grid(column=1, row=0)
    tk.Label(master=root, text="len").grid(column=0, row=1)
    len_ent = tk.Entry(master=root)
    wue.set_vcmd(len_ent, validate_five_or_less_bytelen)
    len_ent.grid(column=1, row=1)
    root.mainloop()


if __name__ == "__main__":
    main()
