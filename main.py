from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from tkinter import messagebox
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import customtkinter as ctk
import pyautogui
import os
import cv2

def main():
    global filename
    app_width = 825
    app_height = 500
    frwidth = 325
    app_font = "Lato"
    filename = None

    screen_width = pyautogui.size()[0]
    screen_height = pyautogui.size()[1]
    
    def openfile():
        global filename
        filename = filedialog.askopenfilename()
        if not str(filename).endswith(('.jpg', '.jpeg', '.png')):
            filename = None
            openerr = messagebox.askretrycancel("Invalid file type", "File not supported. Try again?")
            if openerr:
                openfile()

    def clearfile():
        global filename 
        filename = None

    class Editor(ctk.CTkFrame):
        def __init__(self, master):
            super().__init__(master)
            
            def grayscale():
                img = Image.open(filename)
                img = img.convert("L")
                img.show()
            
            def resize():
                img = Image.open(filename)
                factor = 0.5
                new_image_size = (int(img.size[0]*factor), int(img.size[1]*factor))
                img = img.resize((new_image_size[0], new_image_size[1]))
                img.show()

            def crop():
                img = Image.open(filename)
                img = img.crop((0, 0, 600, 400))
                img.show()

            def simple_blur():
                img = Image.open(filename)
                img = img.filter(ImageFilter.BLUR)
                img.show()

            def brightness():
                img = Image.open(filename)
                img = img.point(lambda p: p * 1.5)
                img.show()
            
            def contrast():
                img = Image.open(filename)
                img = img.point(lambda p: p * 1.5)
                img.show()

            def saturation():
                img = Image.open(filename)
                img = img.point(lambda p: p * 1.5)
                img.show()
            
            def gaussian_blur():
                img = Image.open(filename)
                img = img.filter(ImageFilter.GaussianBlur(5))
                img.show()

            def sharpen():
                img = Image.open(filename)
                img = img.filter(ImageFilter.SHARPEN)
                img.show()

            def edge_detection():
                image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
                sigma1=1.0 
                sigma2=2.0
                
                gaussian1 = cv2.GaussianBlur(image, (0, 0), sigma1)
                gaussian2 = cv2.GaussianBlur(image, (0, 0), sigma2)
                dog = gaussian1 - gaussian2
                dog_normalized = cv2.normalize(dog, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

                plt.figure(figsize=(10, 5))
                plt.subplot(1, 2, 1)
                plt.title('Original Image')
                plt.imshow(image, cmap='gray')
                plt.subplot(1, 2, 2)
                plt.title('Edge Detection (DoG)')
                plt.imshow(dog_normalized, cmap='gray')
                plt.show()

            def ascii_art():
                image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
                width = 100
                height = int((image.shape[0] / image.shape[1]) * width * 0.55) 
                resized_image = cv2.resize(image, (width, height))
                ascii_chars = "@%#*+=-:. "
                ascii_image = []

                for row in resized_image:
                    ascii_row = "".join(ascii_chars[pixel // 32] for pixel in row)
                    ascii_image.append(ascii_row)
                
                plt.figure(figsize=(10, height * 0.15))

                for i, line in enumerate(ascii_image):
                    plt.text(0, height - i - 1, line, fontfamily='monospace', fontsize=8, va='top', ha='left')

                plt.xlim(-1, 1) 
                plt.ylim(-1, height)
                plt.axis('off')
                plt.show()

            def emboss():
                img = Image.open(filename)
                img = img.filter(ImageFilter.EMBOSS)
                img.show()

            def contour():
                img = Image.open(filename)
                img = img.filter(ImageFilter.CONTOUR)
                img.show()

            def enhance():
                img = Image.open(filename)
                factor = 2
                new_image_size = (int(img.size[0]*factor), int(img.size[1]*factor))
                img = img.resize((new_image_size[0], new_image_size[1]), resample=1)
                img.show()

            def instagram_filter1():
                image = Image.open(filename)
                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(1.2)
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.3)
                enhancer = ImageEnhance.Color(image)
                image = enhancer.enhance(1.5)
                enhancer = ImageEnhance.Sharpness(image)
                image = enhancer.enhance(1.2)
                image.show()

            def instagram_filter2():
                image = Image.open(filename)
                image = ImageEnhance.Color(image).enhance(1.8)
                image = ImageEnhance.Brightness(image).enhance(0.9)
                image = ImageEnhance.Contrast(image).enhance(1.4) 
                image = ImageEnhance.Sharpness(image).enhance(1.3)
                image.show()

            def face_detection():
                img = cv2.imread(filename)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.imshow("Face detection", img)
             
            def output():
                if self.effchoice == "Grayscale":
                    grayscale()
                elif self.effchoice == "Resize":
                    resize()
                elif self.effchoice == "Crop":
                    crop()
                elif self.effchoice == "Simple blur":
                    simple_blur()
                elif self.effchoice == "Brightness":
                    brightness()
                elif self.effchoice == "Contrast":
                    contrast()
                elif self.effchoice == "Saturation":
                    saturation()
                elif self.effchoice == "Gaussian blur":
                    gaussian_blur()
                elif self.effchoice == "Sharpen":
                    sharpen()
                elif self.effchoice == "Edge detection":
                    edge_detection()
                elif self.effchoice == "Emboss":
                    emboss()
                elif self.effchoice == "Contour":
                    contour()
                elif self.effchoice == "Face detection":
                    face_detection()
                elif self.effchoice == "Enhance":
                    enhance()
                elif self.effchoice == "Instagram filter 1":
                    instagram_filter1()
                elif self.effchoice == "Instagram filter 2":
                    instagram_filter2()
                elif self.effchoice == "ASCII art":
                    ascii_art()
                elif self.effchoice == "":
                    messagebox.showerror("No effect selected.", "Try selecting an effect from the dropdown menu.")

            def update_editor():
                if filename is None:
                    self.mainlabel.configure(text="")
                    self.output_button.configure(state="disabled")
                    self.effchoice = ""
                    self.effscroll.set(value=(""))
                    self.effscroll.configure(state="disabled")
                    self.imagecon.configure(size=(1, 1))
                    self.imagedisplay.configure(width=480, height=270, text="No image selected.")
                else:
                    self.mainlabel.configure(text="Pick an effect to apply.")
                    self.output_button.configure(state="normal")
                    self.effscroll.configure(state="normal")
                    self.imagecon.configure(dark_image=Image.open(filename), size=(480, 270))
                    self.imagedisplay.configure(image=self.imagecon, text="")
                self.after(500, update_editor)

            def update_choice(choice):
                self.effchoice = choice

            self.effchoice = ctk.StringVar(value="")
            
            self.configure(width=app_width-frwidth, height=app_height)
            self.pack_propagate(0)
            self.pack(expand=True, side="right")
            
            self.imagecon = ctk.CTkImage(dark_image=Image.open(filename), size=(480, 270))

            self.imagedisplay = ctk.CTkLabel(self, image=self.imagecon, text="")
            self.imagedisplay.configure(font=(app_font, 18))
            self.imagedisplay.pack(padx=20, pady=15)            
            
            self.mainlabel = ctk.CTkLabel(self, text="Pick an effect to apply.")
            self.mainlabel.configure(font=(app_font, 18))
            self.mainlabel.pack(padx=20, pady=12)

            self.effscroll = ctk.CTkOptionMenu(self, command=update_choice, variable=self.effchoice, width=150, height=35, 
                                               values=["Grayscale", "Resize", "Crop", "Simple blur", "Brightness", "Contrast", "Saturation", "Gaussian blur", "Sharpen", "Edge detection", "Emboss", "Contour", "Face detection", "Enhance", "Instagram filter 1", "Instagram filter 2", "ASCII art"])
            self.effscroll.pack(padx=20, pady=12)

            self.output_button = ctk.CTkButton(self, text="Apply", command=output, width=150, height=35)
            self.output_button.pack(padx=20, pady=12)

            update_editor()

    class App(ctk.CTk):
        def __init__(self):
            super().__init__()
            
            x = (screen_width - app_width) / 2
            y = (screen_height - app_height) / 2
            
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("assets/custom-theme.json")
            self.title("Image Processing")
            self.geometry(f"{app_width}x{app_height}+{int(x)-100}+{int(y)-100}")
            self.resizable(False, False)       
            
            def update_app():
                filenamelabel = "No image selected"
                if filename is not None:
                    filenamelabel = os.path.basename(filename)
                else:
                    filenamelabel = "No image selected"
                self.filename_label.configure(text=f"File Name: {filenamelabel}")
                if filename is not None:
                    self.open_button.configure(border_color="light green")
                    self.clear_button.configure(state="normal")
                    self.edit_button.configure(state="normal")
                else:
                    self.open_button.configure(border_color="dark red")
                    self.clear_button.configure(state="disabled")
                    self.edit_button.configure(state="disabled")
                self.after(500, update_app)

            def change_theme():
                theme = self.darkmode_switch.get()
                if theme == "light":
                    ctk.set_appearance_mode("light")
                else:
                    ctk.set_appearance_mode("dark")

            def openeditor():
                if filename is None:
                    messagebox.showerror("Error", "No image selected.")
                elif self.editorwin is not None:
                    messagebox.showerror("Error", "Editor window already open.")
                else:
                    self.entryframe.destroy()
                    self.editorwin = Editor(master=self)

            self.mainframe = ctk.CTkFrame(self, width=frwidth, height=app_height)
            self.mainframe.pack_propagate(0)
            self.mainframe.pack(expand=True, side="left")

            self.entryframe = ctk.CTkFrame(self, width=app_width-frwidth, height=app_height)
            self.entryframe.pack_propagate(0)
            self.entryframe.pack(expand=True, side="right")
            
            self.filename_label = ctk.CTkLabel(self.mainframe, text=f"File Name: {filename}")
            self.filename_label.configure(font=(app_font, 19))
            self.filename_label.pack(padx=12, pady=45)
    
            self.open_button = ctk.CTkButton(self.mainframe, text="Open Image", command=openfile, width=150, height=35, border_width=2.5)
            self.open_button.pack(padx=20, pady=15)

            self.edit_button = ctk.CTkButton(self.mainframe, text="Edit the Image", command=openeditor, width=150, height=35)
            self.edit_button.pack(padx=20, pady=15)

            self.clear_button = ctk.CTkButton(self.mainframe, text="Clear Path", command=clearfile, hover=True, hover_color="dark red", width=150, height=35)
            self.clear_button.pack(padx=20, pady=15)
            
            self.exit_button = ctk.CTkButton(self.mainframe, text="Exit", command=self.quit, hover=True, hover_color="dark red", width=150, height=35)
            self.exit_button.pack(padx=20, pady=15)

            self.darkmode_switch = ctk.CTkSwitch(self.mainframe, text="Dark Mode", onvalue="dark", offvalue="light", command=change_theme, font=(app_font, 14))
            self.darkmode_switch.pack(padx=20, pady=15)
            self.darkmode_switch.select("dark")

            self.edmainlabel = ctk.CTkLabel(self.entryframe, text="Welcome to the editor!\n\nPick an image to get started.")
            self.edmainlabel.configure(font=(app_font, 20))
            self.edmainlabel.pack(padx=20, pady=200, anchor="center")

            self.editorwin = None
            update_app()

    top = App()
    top.mainloop()

if __name__ == '__main__':
    main()