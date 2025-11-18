import tkinter as tk
from tkinter import ttk

class BaseSection:
    def __init__(self, parent, controller, selected_operation_var):
        self.parent = parent
        self.controller = controller
        self.selected_operation = selected_operation_var
        self.vars = {}

    def build(self):
        """Build the UI for this section."""
        pass

    def get_handlers(self):
        """Return a dictionary of operation handlers."""
        return {}

    def _build_section(self, title, *, op_key: str | None = None, selector_text: str | None = None):
        frame = ttk.LabelFrame(self.parent, text=title, padding=6)
        frame.pack(fill='x', pady=4)
        if op_key:
            self._add_selector(frame, op_key, selector_text)
        return frame

    def _add_selector(self, frame, op_key: str, selector_text: str | None = None):
        text = selector_text or "Chọn phép này"
        ttk.Radiobutton(
            frame,
            text=text,
            variable=self.selected_operation,
            value=op_key,
        ).pack(anchor='e', pady=(0, 4))

    def _add_scale(
        self,
        parent,
        label,
        var,
        *,
        from_,
        to,
        resolution=1.0,
        format_str: str | None = None,
    ):
        row = ttk.Frame(parent, style="Card.TFrame")
        row.pack(fill='x', pady=2)
        ttk.Label(row, text=label, style="Card.TLabel").pack(anchor='w')
        scale = ttk.Scale(row, variable=var, from_=from_, to=to, orient='horizontal')
        scale.pack(fill='x')

        spin = ttk.Spinbox(
            row,
            textvariable=var,
            from_=from_,
            to=to,
            increment=resolution,
            width=6,
            format=format_str,
        )
        spin.pack(anchor='e', pady=2)
        return scale, spin

    @staticmethod
    def _ensure_odd(size: int) -> int:
        size = max(1, size)
        if size % 2 == 0:
            size += 1
        return size
