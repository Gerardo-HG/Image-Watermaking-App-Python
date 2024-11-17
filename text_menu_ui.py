"""
TextMenu: A class for creating a pop-up window to configure text settings for a watermark application.

This class provides an interface to input text, select text color, font size, and font style. It communicates
these values to the main application via a callback function.

Constants:
- FONTS: A list of available font styles for selection.
- COLORS_AND_CODE: A dictionary mapping color names to their corresponding hexadecimal color codes.

Classes:
- TextMenu: Inherits from `tk.Toplevel` to create a separate pop-up window for text settings.

Attributes:
    in_use (bool): Indicates if an instance of this class is currently open.

Methods:
    __init__(*args, callback=None, **kwargs): Initializes the TextMenu window with the necessary UI components.
    apply_changes(): Validates input fields and passes the configured values to the callback function.
    close_window(): Destroys the TextMenu window and frees resources.
"""
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter.ttk import Combobox

FONTS = [
    "Arial",
    "Verdana",
    "Times New Roman",
    "Courier New",
    "Georgia",
    "Comic Sans MS",
    "Trebuchet MS",
    "Impact",
    "Lucida Console",
    "Tahoma"
]

COLORS_AND_CODE = {
    'Red': "#a32424",
    "Blue": "#2424a3",
    "Yellow": "#e8ff00",
    "Black": "#000000",
    "White": "#ffffff",
}


class TextMenu(tk.Toplevel):
    """
    A pop-up window for configuring text properties such as font, size, color, and content.

    Attributes:
        in_use (bool): Indicates if the window is currently open.
        callback (function): A function to handle the input values (text, color, size, font).

    Methods:
        __init__(*args, callback=None, **kwargs): Initializes the window and creates all UI components.
        apply_changes(): Validates input values and triggers the callback with the selected options.
        close_window(): Closes the window and releases the `grab_set` lock.
    """
    in_use = False

    def __init__(self, *args, callback=None, **kwargs):
        """
        Constructor for the TextMenu class.

        Parameters:
            callback (function): A function that will be invoked with the text settings once the user applies changes.
        """
        super().__init__(*args, **kwargs)
        self.callback = callback
        self.title("Text Menu Settings")
        self.config(padx=40, pady=40)
        self.geometry("500x300")
        self.resizable(False, False)

        # Text Label
        self.text_label = ttk.Label(self, text="Enter a text: ")
        self.text_label.grid(row=0, column=0)

        # Text Entry
        self.text_entry = ttk.Entry(self)
        self.text_entry.grid(row=0, column=1)

        # Color Label
        self.color_label = ttk.Label(self, text="Choose a color:  ")
        self.color_label.grid(row=1, column=0)

        # Color ComboBox
        self.color_box = ttk.Combobox(self, values=[color for color in COLORS_AND_CODE], state='readonly')
        self.color_box.grid(row=1, column=1)

        # Font Size Label
        self.font_size = ttk.Label(self, text="Select a font size:  ")
        self.font_size.grid(row=2, column=0)

        # Font Size SpinBox
        self.spinbox = ttk.Spinbox(self, from_=30, to=80, width=7, state='readonly')
        self.spinbox.grid(row=2, column=1)

        # Font Label
        self.font = ttk.Label(self, text="Select a font:  ")
        self.font.grid(row=3, column=0)

        # Font ComboBox
        self.font_box = ttk.Combobox(self, values=[font for font in FONTS], state='readonly')
        self.font_box.grid(row=3, column=1)

        # Apply Button
        self.apply_button = ttk.Button(self, text="Apply changes", command=self.apply_changes)
        self.apply_button.place(x=150, y=150)

        # Window focus and control
        self.focus()
        self.grab_set()

    def apply_changes(self):
        """
        Validates the input values from the user and sends them to the callback function.

        If any field is incomplete, displays an informational message to complete all fields.
        """
        font_size_value = self.spinbox.get()
        color_value = self.color_box.get()
        text_value = self.text_entry.get()
        font_value = self.font_box.get()

        if font_size_value != '' and color_value != '' and text_value != '' and font_value != '':
            if self.callback:
                self.callback(text_value, COLORS_AND_CODE.get(color_value), font_size_value, font_value)
            self.close_window()
        else:
            tkinter.messagebox.showinfo(
                title="Missing Values",
                message="Please do not leave blank spaces.\nComplete all fields."
            )

    def close_window(self):
        """
        Closes the TextMenu window and releases any resources it is holding.
        """
        self.destroy()
