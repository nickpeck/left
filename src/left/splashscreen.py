from mttkinter import mtTkinter as tk
from PIL import ImageTk, Image


class SplashScreen:

    def __init__(self, title, img_path, duration=6000):
        # from https://github.com/khalil135711/splash_image_code
        self.window = tk.Tk()
        self.window.title(title)

        image_path = img_path
        image = Image.open(image_path)
        background_image = ImageTk.PhotoImage(image)

        background_label = tk.Label(self.window, image=background_image)
        background_label.pack()

        if duration is not None:
            self.window.after(duration, self.close_splash)

        self.window.image = background_image
        self.window.mainloop()

    def close_splash(self):
        self.window.destroy()
