from Abstraction import BaseSearchPanel
from Fetcher import SongAPISync
from tkinter import messagebox
from tkinter import ttk


class SongSearchPanel(BaseSearchPanel):
    def __init__(self, parent, api_key):
        self.api = SongAPISync(api_key)
        super().__init__(parent)

        # Configure modern style
        style = ttk.Style()
        style.configure('Treeview',
                        font=('Segoe UI', 9),
                        rowheight=25,
                        background='#ffffff',
                        fieldbackground='#ffffff',
                        foreground='#333333')
        style.configure('Treeview.Heading',
                        font=('Segoe UI', 9, 'bold'),
                        background='#f0f0f0',
                        foreground='#333333')
        style.map('Treeview',
                  background=[('selected', '#0078d7')],
                  foreground=[('selected', '#ffffff')])

    def columns(self):
        return ["Title", "Artist", "Album"]

    def parse_result_row(self, item):
        return (item["title"], item["artist"]["name"], item["album"]["title"])

    def search_data(self, query):
        return self.api.search_song(query)

    def save_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a song to save.")
            return

        for sel in selected:
            song_data = self.search_results[int(sel)]
            self.api.save_song(song_data)