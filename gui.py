import datetime as dt
import tkinter as tk
from tkinter import CENTER, Frame, TclError, ttk
from typing import Dict, List

from tkcalendar import DateEntry

from data import get_categories_from_dataset, read_csv_file, save_csv_file


class MainWindow(tk.Tk):
    """
    Creates a GUI for the supplied window
    """

    variables: Dict[str, any] = {}
    categories: List[str] = []
    data_file_name: str = None

    def __init__(self, data_file_name: str) -> None:
        super().__init__()

        # Load data file
        self.data_file_name = data_file_name
        data = read_csv_file(self.data_file_name)
        if data is not None:
            # Show this month's summary
            pass

        categories = get_categories_from_dataset(data)
        print("There are {} categories in the dataset".format(len(categories)))

        self.title("Simplistic Personal Budget")
        self.minsize(640, 480)

        self.variables = {
            "date": tk.StringVar(value=dt.datetime.now().strftime("%Y-%m-%d")),
            "amount": tk.DoubleVar(),
            "category": tk.StringVar(),
            "error": tk.StringVar(),
        }

        # Layout for 2 columns, 3 rows
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)

        header_frame = self.create_header_frame(self)
        header_frame.grid(column=0, row=0, sticky="nsew", padx=10, pady=20)

        input_body_frame = self.create_input_body_frame(self, categories)
        input_body_frame.grid(column=0, row=1, sticky="nsew", padx=10, pady=10)

        footer_frame = self.create_footer_frame(self)
        footer_frame.grid(column=0, row=2, sticky="nsew", padx=10, pady=10)

    def create_header_frame(self, window: tk) -> Frame:
        """
        Creates a frame for the header section
        """

        frame = ttk.Frame(window)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame["borderwidth"] = 5

        ttk.Label(
            frame, text="Welcome to Simplistic Personal Budget", anchor=CENTER
        ).grid(column=0, row=0, sticky=tk.N)

        return frame

    def create_input_body_frame(self, window: tk, categories: List[str]) -> Frame:
        """
        Creates a frame for the header section
        """

        frame = ttk.Frame(window)
        # frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=3)
        frame["borderwidth"] = 5

        ttk.Label(frame, text="Date:").grid(column=0, row=0, sticky=tk.W)
        entry_dt = DateEntry(
            frame,
            width=30,
            year=dt.datetime.now().year,
            month=dt.datetime.now().month,
            day=dt.datetime.now().day,
            selectmode="day",
            textvariable=self.variables["date"],
            date_pattern="yyyy-MM-dd",
        )
        entry_dt.grid(column=1, row=0, sticky=tk.W)

        ttk.Label(frame, text="Amount:").grid(column=0, row=1, sticky=tk.W)
        entry_amount = ttk.Entry(frame, width=30, textvariable=self.variables["amount"])
        entry_amount.grid(column=1, row=1, sticky=tk.W)

        ttk.Label(frame, text="Category:").grid(column=0, row=2, sticky=tk.W)
        entry_category = ttk.Combobox(
            frame, width=30, values=categories, textvariable=self.variables["category"]
        )
        entry_category.grid(column=1, row=2, sticky=tk.W)

        return frame

    def create_footer_frame(self, window: tk) -> Frame:
        """
        Creates a frame for the header section
        """

        frame = ttk.Frame(window)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame["borderwidth"] = 5

        ttk.Button(frame, text="Save", command=self.handle_save_clicked).grid(
            column=1, row=0
        )
        ttk.Label(
            frame,
            text="Error message:",
            foreground="#FF0000",
            textvariable=self.variables["error"],
        ).grid(column=0, row=1, columnspan=2)

        return frame

    def handle_save_clicked(self):
        """
        Called when the Save button is clicked
        """

        data_dt = ""
        data_amount = 0.00
        data_category = ""

        try:
            data_dt = dt.datetime.strptime(self.variables["date"].get(), "%Y-%m-%d")
        except Exception as e:
            self.variables["error"].set(e)
            return

        try:
            data_amount = self.variables["amount"].get()
        except TclError as e:
            self.variables["error"].set(e)
            return

        try:
            data_category = str(self.variables["category"].get()).strip()
            if len(data_category) == 0:
                raise TclError("Category must be filled in")

        except TclError as e:
            self.variables["error"].set(e)
            return

        new_row_data = [data_dt, data_amount, data_category]
        dataset = read_csv_file(self.data_file_name)
        dataset.append(new_row_data)
        save_csv_file(self.data_file_name, dataset)

        # Clear the variables
        self.variables["amount"] = 0.00
        self.variables["category"] = ""
