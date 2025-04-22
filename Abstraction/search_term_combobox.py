import tkinter as tk
from tkinter import ttk

class FieldCombobox:
    def __init__(self, parent):
        self.search_field = None
        self.field_dropdown = None
        self.parent = parent
        self.set_ui()

    def set_ui(self):
        # Search field dropdown
        self.search_field = tk.StringVar(self.parent)
        self.search_field.set(self.field()[0])
        self.field_dropdown = ttk.Combobox(self.parent,
                                           textvariable=self.search_field,
                                           values=self.field(),
                                           state="readonly",
                                           width=10,
                                           font=('Segoe UI', 9))
        self.field_dropdown.current(0)


    def field(self)->list:
        """Return list field"""

    def get_value_search_field(self):
        return self.search_field.get().lower()

