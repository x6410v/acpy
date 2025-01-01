from PIL import Image, ImageTk
import tkinter as tk

class CursorOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)

        # Load cursor asset and create transparent background
        self.cursor_img = Image.open('cursor.png').convert("RGBA")
        self.transparent_cursor = Image.new("RGBA", self.cursor_img.size, (0, 0, 0, 0))
        self.transparent_cursor.paste(self.cursor_img, (0, 0), self.cursor_img)

        # Tkinter image with transparency
        self.tk_cursor_img = ImageTk.PhotoImage(self.transparent_cursor)

        self.canvas = tk.Canvas(self.root, width=self.cursor_img.width, height=self.cursor_img.height, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_cursor_img)
        self.root.geometry(f"+0+0")

    def update_cursor_asset(self, x, y):
        self.root.geometry(f"+{int(x)}+{int(y)}")
        self.root.update_idletasks()

    def destroy(self):
        self.root.destroy()