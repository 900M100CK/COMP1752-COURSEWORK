from tkinter import ttk
from Abstraction import FieldCombobox

class SongFields(FieldCombobox):
    def field(self) ->list:
        return ["Title", "Artist", "Album", "All"]

