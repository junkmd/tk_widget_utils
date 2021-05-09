import tkinter as tk

from tk_widget_utils import entries as wue


def main():
    root = tk.Tk()
    tk.Label(master=root, text="alpha").grid(column=0, row=0)
    ent = tk.Entry(master=root)

    def _validate(w: tk.Entry, vp: wue.VcmdParams) -> bool:
        if vp.text_allowed_to_edit.isalpha():
            return True
        if vp.text_allowed_to_edit == "":
            return True
        return False

    wue.set_vcmd(ent, _validate)
    ent.grid(column=1, row=0)
    root.mainloop()


if __name__ == "__main__":
    main()
