from tkinter import ttk

class BaseTable:
    """
    Abstract base class for creating a Treeview table with built-in support for sorting,
    column configuration, and row selection.

    This class provides:
        - Column-based sorting (numeric or alphabetical)
        - Column auto-configuration via `columns()` method
        - UI setup and destruction methods
        - Row selection accessor
        - Hooks for data loading and search logic

    Subclasses must implement:
        - columns(): list of column names
        - load_data(): logic to populate the table
        - (optionally) search(): logic to filter/search data if needed

    Attributes:
        frame (tk.Frame): The parent frame where the Treeview will be rendered.
        table (ttk.Treeview): The main Treeview widget.
        sort_state (dict): Tracks sorting order (ascending/descending) per column.
    """

    def __init__(self, frame):
        self.table = None
        self.frame = frame
        self.status_lbl = None
        self.sort_state = {}
        self.columns = self.columns()
        self.setup_ui()

    def setup_ui(self):
        """
        Initializes and configures the Treeview widget with columns,
        header sort behavior, and a vertical scrollbar.
        """
        self.table = ttk.Treeview(
            self.frame,
            columns=self.columns,
            show="headings",
            selectmode="browse"
        )

        for col in self.columns:
            self.table.heading(col, text=col, anchor="w",
                               command=lambda _col=col: self.sort_column_value(_col, False))
            self.table.column(col, width=105, stretch=True)

        self.table.grid(row=1, column=0,columnspan=2,padx=5, sticky="nsew")
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.table.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.table.configure(yscrollcommand=scrollbar.set)

        self.status_lbl = ttk.Label(self.frame,text="")
        self.status_lbl.grid(row=2, column=0, sticky="nw", pady=10)

    def sort_column_value(self, col, reverse):
        """
        Sorts the table by a given column in ascending or descending order.

        Args:
            col (str): The column name to sort.
            reverse (bool): True for descending order, False for ascending.
        """
        data = []
        for item in self.table.get_children():
            value = self.table.set(item, col)
            data.append((value, item))

        try:
            data.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            data.sort(key=lambda t: t[0].lower(), reverse=reverse)

        for index, (_, item) in enumerate(data):
            self.table.move(item, '', index)

        self.sort_state[col] = not reverse
        self.table.heading(col, command=lambda: self.sort_column_value(col, not reverse))

    def destroy_ui(self):
        """
        Hides or removes the table UI from the layout.
        """
        self.table.grid_forget()

    def columns(self):
        """
        Returns a list of column names for the Treeview table.

        Returns:
            list[str]: Column headers (e.g., ["Title", "Artist", "Album"])
        """
        raise NotImplementedError("Subclasses must implement the columns() method.")

    def load_data(self):
        """
        Loads data into the table. Must be implemented in subclasses.
        """
        pass

