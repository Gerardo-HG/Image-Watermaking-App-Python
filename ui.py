"""
ImageWindowMaker: A class to create a desktop application for adding watermarks to images using Tkinter.

Required Modules:
- os.path
- tkinter (including filedialog and messagebox)
- PIL (Image, ImageTk, ImageDraw, ImageFont)
- text_menu_ui (external class: TextMenu)

Constants:
- BACKGROUND_COLOR: Background color of the main window.
- FRONT_COLOR: Background color of the application canvas.

Classes:
- ImageWindowMaker: Inherits from `tk.Tk` and handles the complete graphical interface logic for selecting, editing, and saving images with watermarks.
"""

import os.path
from tkinter import *
import tkinter.filedialog, tkinter.messagebox
import tkinter as tk
from text_menu_ui import TextMenu
from PIL import Image, ImageTk, ImageDraw, ImageFont


BACKGROUND_COLOR = "#fcf3cf"
FRONT_COLOR = "#f6ddcc"


class ImageWindowMaker(tk.Tk):
    """
    Main class for creating an application that adds watermarks to images.

    Attributes:
        in_principal (bool): Indicates whether the user is on the main screen.
        canvas (tk.Canvas): Canvas to display graphical elements.
        app_title (int): ID of the main text on the canvas.
        app_image (tk.PhotoImage): Icon image loaded on the main canvas.
        search_file (str): Path of the selected image file.
        new_image (ImageTk.PhotoImage): Resized image loaded onto the canvas.
        text_watermarker (int): ID of the watermark text on the canvas.
        watermark_text (str): Watermark text entered by the user.
        text_color (str): Selected color for the watermark text.
        font_size (int): Font size for the watermark text.
        font_value (str): Selected font for the watermark text.

    Methods:
        __init__(*args, **kwargs): Initializes the main window.
        menu_start(): Loads the main interface for selecting images.
        change_menu(): Switches the interface to allow editing of the selected image.
        add_image(): Loads the selected image and resizes it to fit the canvas.
        save_image(): Saves the image with the watermark to the selected location.
        setting_buttons(state): Configures the interface buttons based on the current state.
        return_to_principal(): Returns to the main screen and resets graphical elements.
        open_text_settings(): Opens a secondary window for entering watermark data.
        values_received(r_text, r_color_text, r_font_size, r_font_value): Receives watermark values and applies them to the canvas.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor for the class. Configures the main window and loads the initial screen.
        """
        super().__init__(*args, **kwargs)
        self.title("Image Watermarking App")
        self.config(padx=40, pady=40, bg=BACKGROUND_COLOR)
        self.in_principal = True
        self.menu_start()
        self.mainloop()

    def menu_start(self):
        """
        Configures the main screen to allow image selection.
        """
        # Creating the canvas and graphical elements
        self.canvas = Canvas(width=600, height=600)
        self.app_title = self.canvas.create_text(300, 100, text='Add a Watermark', font=('TkMenuFont', 30, 'bold'))
        self.app_image = PhotoImage(file="images/watermaker_icon.png")
        self.logo = self.canvas.create_image(300, 300, image=self.app_image)
        self.canvas.config(bg=FRONT_COLOR, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=2)

        # Button to select file
        self.select_file_button = Button(text="Select File", highlightthickness=0, command=self.change_menu, width=10)
        self.select_file_button.grid(row=1, column=0, columnspan=2, pady=15)

        # Credits label
        self.credit_label = Label(text='Desktop App Made by Gerardo-HG', fg='white', font=("Ariel", 20, "bold"))
        self.credit_label.grid(row=2, column=0, columnspan=2, pady=25)

    def change_menu(self):
        """
        Allows the user to select an image and switches to the editing interface if a valid file is selected.
        """
        self.search_file = tkinter.filedialog.askopenfilename(title='Select Image File',
                                                              filetypes=[("Image Files", "*.png")])

        if self.in_principal and self.search_file != '':
            self.in_principal = False
            self.canvas.delete(self.app_title)
            self.credit_label.grid_forget()
            self.setting_buttons(self.in_principal)
            self.add_image()

    def add_image(self):
        """
        Loads the selected image onto the canvas and resizes it to 600x600 pixels.
        """
        self.text_watermarker = self.canvas.create_text(300, 500, width=500, text="")
        new_image = Image.open(self.search_file)
        resized_image = new_image.resize((600, 600))
        self.new_image = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.logo, image=self.new_image)

    def save_image(self):
        """
        Saves the edited image with the watermark to the user-selected location.
        """
        file_to_save = tkinter.filedialog.asksaveasfile(mode='w', defaultextension='.png',
                                                        filetypes=(("PNG file", "*.png"), ("All File", "*.*")))
        if file_to_save:
            abs_path = os.path.abspath(file_to_save.name)
            editable_image = Image.open(self.search_file).resize((600, 600))
            draw = ImageDraw.Draw(editable_image)

            text_value = self.canvas.itemcget(self.text_watermarker, "text")

            font_path = "path_to_font.ttf"
            try:
                font = ImageFont.truetype(font_path, int(self.font_size))
            except IOError:
                font = ImageFont.load_default()

            draw.text((300, 500), text_value, fill=self.text_color, font=font, anchor="ms")
            editable_image.save(abs_path)
            tk.messagebox.showinfo(title="Image saved", message=f"File saved correctly.")
            print(f"Image saved in: {abs_path}")

    def setting_buttons(self, state):
        """
        Configures the interface buttons based on the current state (main screen or editing).
        """
        if not state:
            self.select_file_button.grid_forget()

            # Button to insert text
            self.insert_text_button = Button(text="Insert a text", highlightthickness=0,
                                             command=self.open_text_settings, width=10)
            self.insert_text_button.grid(row=1, column=0, pady=15, padx=15)

            # Button to save the image
            self.save_button = Button(text="Save Image", highlightthickness=0, command=self.save_image, width=10)
            self.save_button.grid(row=1, column=1, pady=15, padx=15)

            # Button to return
            self.return_button = Button(text='Return', highlightthickness=0, command=self.return_to_principal, width=10)
            self.return_button.grid(row=0, column=2, padx=15)

    def return_to_principal(self):
        """
        Resets the main screen and its graphical elements.
        """
        self.in_principal = True
        self.insert_text_button.grid_forget()
        self.return_button.grid_forget()
        self.save_button.grid_forget()
        self.menu_start()

    def open_text_settings(self):
        """
        Opens a secondary window to configure the watermark text.
        """
        if not TextMenu.in_use:
            self.text_window = TextMenu(callback=self.values_received)

    def values_received(self, r_text, r_color_text, r_font_size, r_font_value):
        """
        Receives and applies the values entered in the secondary window.

        Parameters:
            r_text (str): The watermark text.
            r_color_text (str): Hexadecimal code for the selected text color.
            r_font_size (int): The selected font size.
            r_font_value (str): The selected font name.
        """
        self.watermark_text = r_text
        self.text_color = r_color_text
        self.font_size = r_font_size
        self.font_value = r_font_value

        self.canvas.itemconfig(self.text_watermarker, text=r_text, fill=r_color_text,
                               font=(r_font_value, r_font_size, "bold"))
