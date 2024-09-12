from mttkinter import mtTkinter as tk
from PIL import ImageTk, Image
from screeninfo import get_monitors


class SplashScreen:

    def __init__(self, title, img_path, duration=6000):
        # from https://github.com/khalil135711/splash_image_code
        self.window = tk.Tk()
        self.window.title(title)
        self.window.overrideredirect(True)

        image_path = img_path
        image = Image.open(image_path)
        background_image = ImageTk.PhotoImage(image)

        self.window.geometry(
            f"{image.width}x{image.height}+{(get_monitors()[0].width - image.width) // 2}+{(get_monitors()[0].height - image.height) // 2}")

        background_label = tk.Label(self.window, image=background_image)
        background_label.pack()

        if duration is not None:
            self.window.after(duration, self.close_splash)

        self.window.image = background_image
        self.window.mainloop()

    def close_splash(self):
        self.window.destroy()
