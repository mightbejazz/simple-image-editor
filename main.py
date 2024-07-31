from PIL import Image
import customtkinter as ctk
import pyautogui
import os
from tkinter import messagebox
from tkinter import filedialog

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
             
            def output():
                if self.effchoice == "Grayscale":
                    grayscale()
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

            self.effscroll = ctk.CTkOptionMenu(self, values=["Grayscale"], command=update_choice, variable=self.effchoice, width=150, height=35)
            self.effscroll.pack(padx=20, pady=12)

            self.output_button = ctk.CTkButton(self, text="Display Output", command=output, width=150, height=35)
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

            self.edit_button = ctk.CTkButton(self.mainframe, text="Edit the image", command=openeditor, width=150, height=35)
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