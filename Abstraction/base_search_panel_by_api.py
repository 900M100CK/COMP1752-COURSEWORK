import tkinter as tk
from tkinter import ttk

class BaseSearchPanel:
    """
    Abstract base class for building a reusable search UI panel with a Treeview table.

    Subclasses must implement:
        - columns(): Returns a list of column names.
        - parse_result_row(item): Parses a raw result into a tuple for display.
        - search_data(query): Fetches raw results from a data source (API or DB).
    """

    def __init__(self, parent):
        self.parent = parent
        self.frame = None
        self.status_lbl =None
        self.form_search = None
        self.table_frame = None
        self.entry = None
        self.search_btn = None
        self.save_btn = None
        self.query_var = None
        self.search_results = []
        self.table = None
        self.setup_ui()

    def setup_ui(self):
        """Builds the search panel UI (entry, button, table, save button)."""
        self.frame = ttk.Frame(self.parent, padding=10)
        self.frame.grid(row=1, column=0, sticky="nsew")

        # Search input
        self.form_search = ttk.Frame(self.frame)
        self.form_search.grid(row=0, column=0, sticky="ew")
        self.query_var = tk.StringVar(self.form_search)
        self.entry = ttk.Entry(self.form_search, textvariable=self.query_var, width=40)
        self.entry.grid(row=0, column=1, padx=5)
        self.entry.bind("<Return>", self.search)

        # Search button
        self.search_btn = ttk.Button(self.form_search, text="Search", command=self.search)
        self.search_btn.grid(row=0, column=2)

        # Treeview table
        self.table_frame = ttk.Frame(self.frame)
        self.table_frame.grid(row=1, column=0, sticky="nsew")
        self.table = ttk.Treeview(self.table_frame, columns=self.columns(), show="headings", height=12)
        self.table.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")
        for col in self.columns():
            self.table.heading(col, text=col)

        # Save selected button
        self.save_btn = ttk.Button(self.frame, text="Save Selected", command=self.save_selected)
        self.save_btn.grid(row=3, column=0, columnspan=2, pady=5)

        # Status when Add Song is clicked
        self.status_lbl = ttk.Label(self.frame, text="")
        self.status_lbl.grid(row=4, column=0,sticky="nw", pady=5)

    def destroy_ui(self):
        """Removes the panel UI from the layout."""
        if self.frame:
            self.frame.grid_forget()

    def columns(self):
        """
        Returns a list of column names for the Treeview table.

        Returns:
            list[str]: Column headers (e.g., ["Title", "Artist", "Album"]).
        """
        raise NotImplementedError("Subclasses must implement the columns() method.")

    def parse_result_row(self, item):
        """
        Converts a raw data item into a tuple of values to display in the table.

        Args:
            item (dict): A result item returned from the data source (API/DB).

        Returns:
            tuple: A row of data matching the order of the columns.
        """
        raise NotImplementedError("Subclasses must implement the parse_result_row(item) method.")

    def search_data(self, query):
        """
        Executes a search using the given query.

        Args:
            query (str): The keyword or search phrase.

        Returns:
            list[dict]: A list of raw result dictionaries from the data source.
        """
        raise NotImplementedError("Subclasses must implement the search_data(query) method.")

    def search(self, event=None):
        """
        Triggers the search using the input query and loads the result into the table.
        """
        query = self.query_var.get().strip()
        if not query:
            return

        self.search_results = self.search_data(query)
        self.load_data()

    def load_data(self):
        """
        Loads `search_results` into the Treeview table.
        """
        self.table.delete(*self.table.get_children())
        for i, item in enumerate(self.search_results):
            self.table.insert("", "end", iid=i, values=self.parse_result_row(item))

    def save_selected(self):
        """
        Handles the "Save Selected" action. Default behavior: print parsed data.
        Subclasses can override this to persist data to a database or file.
        """
        selected = self.table.selection()
        for sel in selected:
            item = self.search_results[int(sel)]
            print(f"[INFO] Saving: {self.parse_result_row(item)}")
