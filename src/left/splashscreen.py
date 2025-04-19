from mttkinter import mtTkinter as tk
from PIL import ImageTk, Image
from screeninfo import get_monitors

from typing import Optional


class SplashScreen:

    window: Optional[tk.TK] = None
    image: Optional[Image] = None

    def __init__(self, title, img_path, duration=6000):
        # from https://github.com/khalil135711/splash_image_code
        self._open_splash(title, img_path)
        if duration is not None:
            self.window.after(duration, self._close_splash)
        self.window.mainloop()

    def _open_splash(self, title,  img_path):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.overrideredirect(True)
        self.image = self._load_image(img_path)
        self._set_background_image(img_path)

    @staticmethod
    def _load_image(img_path):
        image_path = img_path
        return Image.open(image_path)

    def _set_background_image(self):
        background_image = ImageTk.PhotoImage(self.image)
        self.window.geometry(
            f"{self.image.width}x{self.image.height}+{(get_monitors()[0].width - self.image.width) // 2}+"
            f"{(get_monitors()[0].height - self.image.height) // 2}")
        background_label = tk.Label(self.window, image=background_image)
        background_label.pack()
        self.window.image = background_image

    def _close_splash(self):
        self.window.destroy()
